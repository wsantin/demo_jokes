from sqlalchemy import Column, String, ForeignKey, Enum, Date, Text, SmallInteger, Boolean,\
    Float, Integer, and_, or_, func, Numeric, TIMESTAMP, ARRAY, JSON
from sqlalchemy.orm import Session, relationship, backref
from typing import List

from app.database.session import Base

from app.models.timestamp import TimestampMixin
from app.models.id import IdHex, IdUuid, IdInt, type_id_uuid, type_id_hex, type_id_int
from app.models.user.user import UserModel

from app.exceptions.fast_api_custom import CustomException

class WhitListedApi(TimestampMixin, IdHex, Base):
  __tablename__ = "WhitlistedApi"
  
  user_id = Column(type_id_int, ForeignKey('Users.id'), nullable=False)
  ip = Column( String(200), nullable=False, unique=True)

  # Relations
  # user = relationship( "UserModel", lazy="joined", uselist=False, backref=backref("user", cascade="all, delete-orphan"), remote_side="UserModel.id" )

  def __init__(self, **kwargs):
    super(WhitListedApi, self).__init__(**kwargs)

  def __hash__(self):
    return hash(self.id)