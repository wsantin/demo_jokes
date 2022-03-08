from sqlalchemy import Column, String, ForeignKey, Enum, Date, Text, SmallInteger, Boolean,\
    Float, Integer, and_, or_, func, Numeric, TIMESTAMP, ARRAY, JSON, DateTime
from sqlalchemy.orm import Session, relationship, backref
from typing import List

from app.database.session import Base

from app.models.timestamp import TimestampMixin
from app.models.id import IdHex, IdUuid, IdInt, type_id_uuid, type_id_hex, type_id_int
from app.models.message import MessageModel
from app.models.country import CountryModel

from app.exceptions.fast_api_custom import CustomException

class MessageDetailModel(TimestampMixin, IdInt, Base):
  __tablename__ = "MessagesDetails"
  
  message_id = Column(type_id_int, ForeignKey('Messages.id'), nullable=False, index=True)
  country_id = Column(type_id_int, ForeignKey('Countries.id'), nullable=True, index=True)
  phone = Column( String(50), nullable=False, index=True)
  sent_at = Column(DateTime)
  readed_at = Column(DateTime)
  status = Column(Enum('schedule', 'create', 'in_process', 'sent', 'failed', 'canceled', name='enum_message_status'), default='create', nullable=False, index=True)
  price = Column(Float)
  price_real = Column(Float)
  description = Column(String(250))
  description_admin =Column(Text)

  # Relations
  message = relationship(MessageModel, backref=backref("message_detail", lazy='dynamic'))
  country = relationship(CountryModel, backref=backref("message_detail", lazy='dynamic'))

  def __init__(self, **kwargs):
    super(MessageDetailModel, self).__init__(**kwargs)

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
    return cls.query.filter_by(id = id, disabled_at=None).first()

  @classmethod
  def read_all_by_message_id(cls, message_id: str):
    return cls.query.filter_by(message_id = message_id, disabled_at=None).order_by(cls.status.desc()).all()
  
  @classmethod
  def read_disabled(cls, id: str):
    return cls.query.filter_by(id = id).first()
  
  @classmethod
  def read_select(cls):
    return cls.query.filter_by(disabled_at=None).all()
  
  @classmethod
  def read_paginate(cls, args):
    ### QUERY BASE
    pagination = cls.query

    sort = None

    ### GET SORT
    if args.sort_by == 'phone':
      sort = cls.phone
    elif args.sort_by == 'status':
      sort = cls.status
    elif args.sort_by == 'price':
      sort = cls.price
    elif args.sort_by == 'description':
      sort = cls.description

    if sort:
      if args.order == 'asc':
        pagination = pagination.order_by(sort.asc())
      if args.order == 'desc':
        pagination = pagination.order_by(sort.desc())
    else:
      # pagination = pagination.order_by(cls.updated_at.desc()) 
      pagination = pagination.order_by(cls.created_at.desc()) 

    ### FILTER
    search = "%{}%".format(args.search)
    pagination = pagination.filter(or_(cls.phone.ilike(search),
                                       cls.status.ilike(search),
                                       cls.price.ilike(search),
                                       cls.description.ilike(search)
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
  