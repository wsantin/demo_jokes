import smtplib
from sqlalchemy import Column, String, ForeignKey, Enum, Date, Text, SmallInteger, Boolean,\
    Float, Integer, and_, or_, func, Numeric, TIMESTAMP, ARRAY, JSON, DateTime
from sqlalchemy.orm import Session, relationship, backref
from typing import List

from app.database.session import Base

from app.models.timestamp import TimestampMixin
from app.models.id import IdHex, IdUuid, IdInt, type_id_uuid, type_id_hex, type_id_int

from app.configs.environment import Config
from app.exceptions.fast_api_custom import CustomException

class UserModel(TimestampMixin, IdInt, Base):
  __tablename__ = "Users"
  
  code_affiliate = Column( String(20))
  telegram = Column(String(50), unique=True, nullable=True, index=True)
  name = Column(String(50), nullable=False)
  email = Column(String(100), nullable=False, unique=True, index=True)
  password = Column(String(250), nullable=False)
  phone = Column(String(15), unique=True, index=True)
  sender_default = Column( String(20))
  api_key = Column( String(150), unique=True, index=True)
  api_secret = Column( String(150), unique=True, index=True)
  nivel = Column(Enum('admin', 'operador', 'customer', name='enum_user_nivel'), default='customer', nullable=False, index=True)
  status = Column(Enum('code', 'pending', 'aproved', 'change_password', 'desactivate', 'desactivate_bot', name='enum_user_status'), default='pending', nullable=False, index=True)
  aproved_code =  Column( String(50))
  aproved_expire_at = Column( DateTime(timezone=True))
  aproved_qty =  Column( Integer, default=0)
  aproved_reload_at = Column( DateTime(timezone=True))
  attempts_allowed_qty =  Column( Integer, default=0)
  attempts_allowed_date =  Column( DateTime)
  observation = Column( String(150))

  aproved_user_id = Column(type_id_int, ForeignKey('Users.id'), nullable=True, index=True)
  referrer_user_id = Column(ForeignKey('Users.id'), nullable=True, index=True)

  # back_populates="parent"

  # Relations
  # user_aproved = relationship( "UserModel", lazy="joined", uselist=False, backref=backref("user", cascade="all, delete-orphan"), remote_side="UserModel.id" )
  # referrer = relationship( "UserModel", lazy="joined", uselist=False, backref=backref("user", cascade="all, delete-orphan"), remote_side="UserModel.id" )
  # referrer_user = relationship("UserModel",  uselist=False, viewonly=True, lazy="joined")
  referrer_user = relationship("UserModel",  foreign_keys=referrer_user_id, viewonly=True)

  def __init__(self, **kwargs):
    super(UserModel, self).__init__(**kwargs)

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
  def read_by_email(cls, email: str):
    return cls.query.filter(cls.email == email).first()

  @classmethod
  def read_by_code_affiliate(cls, code_affiliate: str):
    return cls.query.filter(cls.code_affiliate == code_affiliate, cls.status.in_(["aproved", "pending", "change_password"])).first()

  @classmethod
  def read_disabled(cls, id: str):
    return cls.query.filter_by(id = id).first()
  
  @classmethod
  def read_select(cls):
    return cls.query.filter_by(disabled_at=None).all()
  
  @classmethod
  def read_paginate(cls, args, type_user=None):
    ### QUERY BASE
    pagination = cls.query

    if(type_user):
      pagination = pagination.filter(cls.nivel == type_user)

    sort = None

    ### GET SORT
    if args.sort_by == 'name':
      sort = cls.name
    elif args.sort_by == 'email':
      sort = cls.email
    elif args.sort_by == 'phone':
      sort = cls.phone
    elif args.sort_by == 'email':
      sort = cls.email
    elif args.sort_by == 'status':
      sort = cls.status

    if sort:
      if args.order == 'asc':
        pagination = pagination.order_by(sort.asc())
      if args.order == 'desc':
        pagination = pagination.order_by(sort.desc())
    else:
      pagination = pagination.order_by(cls.updated_at.desc()) 
      # pagination = pagination.order_by(cls.created_at.desc()) 

    ### FILTER
    search = "%{}%".format(args.search)
    pagination = pagination.filter(or_(cls.name.ilike(search),
                                       cls.email.ilike(search),
                                       cls.phone.ilike(search),
                                       cls.email.ilike(search),
                                       cls.status.ilike(search)
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
  