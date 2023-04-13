from sqlalchemy import Column, String,  or_, func
from sqlalchemy.orm import Session

from app.database.session import Base

from app.models.timestamp import TimestampMixin
from app.models.id import IdInt

from app.exceptions.fast_api_custom import CustomException

class JokesModel(TimestampMixin, IdInt, Base):
  """ JokesModel  """
  __tablename__ = "jokes"

  description = Column( String(150))

  def __init__(self, **kwargs):
    super(JokesModel, self).__init__(**kwargs)

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
        detail='No es posible eliminar el registro, debido a que no se encuentra disponible ó ha sido eliminado.')
    
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
    if args.sort_by == 'description':
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
    pagination = pagination.filter(or_(cls.last_name.ilike(search),
                                       cls.first_name.ilike(search),
                                       cls.phone.ilike(search),
                                       cls.description.ilike(search)))
    
    pagination = pagination.paginate(page=int(args.page), per_page=int(args.per_page), error_out=False)
    return pagination
  
  @classmethod
  def delete(cls, db_session: Session, id: str):
    query = cls.query.filter_by(id=id, disabled_at=None).first()
    
    if query is None:
      raise CustomException(status_code=404, type='NoData', 
        detail='No es posible eliminar el registro, debido a que no se encuentra disponible ó ha sido eliminado.')
    
    query.disabled_at = func.now()
    db_session.flush()
    return query
  
  @classmethod
  def restore(cls, db_session: Session, id: str):
    query = cls.query.filter(cls.id==id, cls.disabled_at.isnot(None)).first()
    
    if query is None:
      raise CustomException(status_code=404, type='NoData', 
        detail='No es posible restaurar el registro, debido a que no se encuentra disponible ó ha sido eliminado.')
    
    query.disabled_at = None
    db_session.flush()
    return query
  