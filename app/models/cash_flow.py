from sqlalchemy import Column, String, ForeignKey, Enum, Date, Text, SmallInteger, Boolean,\
    Float, Integer, and_, or_, func, Numeric, TIMESTAMP, ARRAY, JSON, desc
from sqlalchemy.orm import Session, relationship, backref
from typing import List

from app.database.session import Base

from app.models.timestamp import TimestampMixin
from app.models.id import IdHex, IdUuid, IdInt, type_id_uuid, type_id_hex, type_id_int
from app.models.user import UserModel

from app.exceptions.fast_api_custom import CustomException

class CashFlowModel(TimestampMixin, IdInt, Base):
  __tablename__ = "CashFlows"
  # __table_args__ = {'extend_existing': True}
  
  code = Column( String(250), unique=True, index=True)
  user_id = Column(type_id_int, ForeignKey('Users.id'), nullable=False, index=True)
  service = Column(String(50))
  credit_amount = Column(Float, default=0)
  output_amount = Column(Float, default=0)
  motive = Column( String(250), nullable=False)
  credit_total = Column(Float, nullable=False, default=0)
  status = Column(Enum('pending', 'approved', 'not_approved', name='enum_transaction'), default='pending', nullable=False)
  observation = Column( String(150))

  reference_user_id = Column(type_id_int, ForeignKey('Users.id'), nullable=True, index=True)
  approved_user_id = Column(type_id_int, ForeignKey('Users.id'), nullable=True, index=True)

  # # Relations
  #user = relationship(UserModel, backref=backref("user", lazy='dynamic'))
  # reference_user = relationship( "UserModel", lazy="joined", uselist=False, backref=backref("user", cascade="all, delete-orphan"), remote_side="UserModel.id" )
  # approved_user = relationship( "UserModel", lazy="joined", uselist=False, backref=backref("user", cascade="all, delete-orphan"), remote_side="UserModel.id" )
  
  # user =  relationship("UserModel",  foreign_keys=[user_id], backref=backref("cash_flows", lazy='dynamic'))
  user = relationship("UserModel", foreign_keys=user_id, backref=backref("cash_flow", lazy='dynamic'))
  # user = referrer = relationship("UserModel", backref=backref("cash_flow", lazy='dynamic'))
  reference_user =  relationship("UserModel",  uselist=False, foreign_keys=reference_user_id)
  approved_user =  relationship("UserModel",  uselist=False, foreign_keys=approved_user_id)
  
  __mapper_args__ = {"inherit_condition": id==UserModel.id}

  def __init__(self, **kwargs):
    super(CashFlowModel, self).__init__(**kwargs)

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
  def read_by_user_id(cls, user_id: str, limit=None, orderBy=None):
    query = cls.query.filter(cls.user_id == user_id)

    if orderBy == 'id':
      query = query.order_by(cls.id.desc())
    else:
      query = query.order_by(cls.created_at.desc())

    if limit:
      query = query.limit(limit)
    return query.all()
  
  @classmethod
  def read_current_balance(cls, user_id: str):
    return cls.query.filter(cls.user_id == user_id).order_by(cls.id.desc()).first()

  @classmethod
  def read_last_recharge(cls, user_id: str):
    return cls.query.filter(cls.user_id == user_id, cls.output_amount==0 ).order_by(cls.id.desc()).first()
  
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
    if args.sort_by == 'service':
      sort = cls.service
    elif args.sort_by == 'motive':
      sort = cls.motive
    elif args.sort_by == 'status':
      sort = cls.status
    elif args.sort_by == 'observation':
      sort = cls.observation

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
    pagination = pagination.filter(or_(cls.service.ilike(search),
                                       cls.motive.ilike(search),
                                       cls.status.ilike(search),
                                       cls.observation.ilike(search)
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
  