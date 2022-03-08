from sqlalchemy import Column, String, ForeignKey, Enum, Date, Text, SmallInteger, Boolean,\
    Float, Integer, and_, or_, func, Numeric, TIMESTAMP, ARRAY, JSON
from sqlalchemy.orm import Session, relationship, backref
from typing import List

from app.database.session import Base

from app.models.timestamp import TimestampMixin
from app.models.id import IdHex, IdUuid, IdInt, type_id_uuid, type_id_hex
from app.models.user import UserModel

from app.exceptions.fast_api_custom import CustomException

class GatewayModel(TimestampMixin, IdInt, Base):
  __tablename__ = "Gateways"
  
  code = Column( String(50), unique=True, index=True)
  # type = Column(Enum('messages', 'call' name='enum_gateway'), default='question', nullable=False)
  description = Column(String(250), nullable=False)
  description_admin = Column(String(250), nullable=True)
  status = Column(Boolean, default=True)

  def __init__(self, **kwargs):
    super(GatewayModel, self).__init__(**kwargs)

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
    if args.sort_by == 'last_name':
      sort = cls.last_name
    elif args.sort_by == 'first_name':
      sort = cls.first_name
    elif args.sort_by == 'phone':
      sort = cls.phone
    elif args.sort_by == 'dni':
      sort = cls.dni
    elif args.sort_by == 'email':
      sort = cls.email

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
    pagination = pagination.filter(or_(cls.last_name.ilike(search),
                                       cls.first_name.ilike(search),
                                       cls.phone.ilike(search),
                                       cls.dni.ilike(search),
                                       cls.email.ilike(search)
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
  