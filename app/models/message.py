from sqlalchemy import Column, String, ForeignKey, Enum, Date, Text, SmallInteger, Boolean,\
    Float, Integer, and_, or_, func, Numeric, TIMESTAMP, ARRAY, JSON, DateTime
from sqlalchemy.orm import Session, relationship, backref
from typing import List

from app.database.session import Base

from app.models.timestamp import TimestampMixin
from app.models.id import IdHex, IdUuid, IdInt, type_id_uuid, type_id_hex, type_id_int
from app.models.user import UserModel
from app.models.gateway import GatewayModel

from app.exceptions.fast_api_custom import CustomException

class MessageModel(TimestampMixin, IdInt, Base):
  __tablename__ = "Messages"
  
  user_id = Column(type_id_int, ForeignKey('Users.id'), nullable=False, index=True)
  gateway_id = Column(type_id_int, ForeignKey('Gateways.id'), nullable=False, index=True)
  sender = Column( String(150), nullable=False)
  message = Column( String(250), nullable=False)
  type = Column(Enum('sms', 'whatsapp', name='enum_message_type'), default='question', nullable=False)
  status = Column(Enum('schedule', 'create', 'in_process', 'some_not_sent', 'all_sent', 'error', 'canceled', name='enum_message_status'), default='create', nullable=False, index=True)
  schedule_date = Column(DateTime)
  ip = Column(String(20), nullable=False) 
  sent_from = Column(Enum('web', 'api', name='enum_message_sent_from'), nullable=False, index=True)
  
  # Relations
  user = relationship(UserModel, backref=backref("message", lazy='dynamic'))
  # user = relationship("UserModel", backref="message")
  gateway = relationship(GatewayModel, backref=backref("message", lazy='dynamic'))


  def __init__(self, **kwargs):
    super(MessageModel, self).__init__(**kwargs)

  def __hash__(self):
    return hash(self.id)

  @classmethod
  def create(cls, db_session: Session, **kwargs):
    new = cls(**kwargs)
    db_session.add(new)
    db_session.flush()
    return new
  
  @classmethod
  def update(cls, db_session: Session, id: str,  **kwargs):
    query = cls.query.filter_by(id=id, disabled_at=None).first()
    
    if query is None:
      raise CustomException(status_code=404, type='NoData',
        detail='No es posible eliminar el registro, debido a que no se encuentra disponible ó ha sido desactivado.')
    
    for key, value in kwargs.items():
        if hasattr(query, key):
          setattr(query, key, value)

    db_session.flush()
    return query

  @classmethod
  def read(cls, id: str):
    query = cls.query.filter_by(id = id, disabled_at=None).first()
  
  @classmethod
  def read_by_user_id(cls, user_id: str, limit= None, orderBy=None):
    query = cls.query.filter(cls.user_id == user_id)

    if orderBy == 'id':
      query = query.order_by(cls.id.desc())
    else:
      query = query.order_by(cls.created_at.desc())

    if limit:
      query = query.limit(limit)
    return query.all()
    
  @classmethod
  def read_disabled(cls, id: str):
    return cls.query.filter_by(id = id).first()
  
  @classmethod
  def read_select(cls):
    return cls.query.filter_by(disabled_at=None).all()
  
  @classmethod
  def read_paginate(cls, query, args):
    ### QUERY BASE
    pagination = query

    sort = None

    ### GET SORT
    if args.sort_by == 'sender':
      sort = cls.sender
    elif args.sort_by == 'status':
      sort = cls.status
    elif args.sort_by == 'ip':
      sort = cls.ip
    elif args.sort_by == 'sent_from':
      sort = cls.sent_from

    if sort:
      if args.order == 'asc':
        pagination = pagination.order_by(sort.asc())
      if args.order == 'desc':
        pagination = pagination.order_by(sort.desc())
    else:
      # pagination = pagination.order_by(cls.updated_at.desc()) 
      pagination = pagination.order_by(cls.id.desc()) 

    ### FILTER
    search = "%{}%".format(args.search)
    pagination = pagination.filter(or_(cls.sender.ilike(search),
                                       cls.status.ilike(search),
                                       cls.ip.ilike(search),
                                       cls.sent_from.ilike(search)
                                      ))
    
    pagination = pagination.paginate(page=int(args.page), per_page=int(args.per_page), error_out=False)
    return pagination
  
  @classmethod
  def delete(cls, db_session: Session, id: str):
    query = cls.query.filter_by(id=id, disabled_at=None).first()
    
    if query is None:
      raise CustomException(status_code=404, type='NoData', 
        detail='No es posible eliminar el registro, debido a que no se encuentra disponible ó ha sido desactivado.')
    
    query.disabled_at = func.now()
    db_session.flush()
    return query
  
  @classmethod
  def restore(cls, db_session: Session, id: str):
    query = cls.query.filter(cls.id==id, cls.disabled_at.isnot(None)).first()
    
    if query is None:
      raise CustomException(status_code=404, type='NoData', 
        detail='No es posible restaurar el registro, debido a que no se encuentra disponible ó ha sido desactivado.')
    
    query.disabled_at = None
    db_session.flush()
    return query
  