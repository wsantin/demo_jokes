from datetime import datetime
from typing import Optional, Callable, Generic

from pydantic import BaseModel, EmailStr, Field, validator, UUID4, conint
from app.schemas.message import MessageSchema
from app.schemas.country import CountryCodeSchema

class MessageDetailSchema(BaseModel):
  id: Optional[int]
  # message_id: int
  phone: str
  sent_at: Optional[datetime]
  readed_at: Optional[datetime]
  status: str
  price: Optional[float]
  # price_real: Optional[float]
  description: Optional[datetime]
  description_admin: Optional[datetime]

  # message: MessageSchema = None
  country: CountryCodeSchema = None

  created_at: Optional[datetime]
  # updated_at: Optional[datetime]
  disabled_at: Optional[datetime]


  class Config:
    orm_mode = True
    arbitrary_types_allowed = True

class MessageDetailValidate(BaseModel):
  last_name: str = Field(..., max_length=50)
  first_name: str = Field(..., max_length=50)
  phone:  str = Field(..., min_length=9, max_length=20)
  description: Optional[str] = Field('', min_length=2, max_length=150)
  
  @validator('*', pre=True)
  @classmethod
  def blank_strings(cls, v):
    if type(v) == str:  
      if v == "":
        return None
      elif v == None:
        return None
      return v.strip()
    
    return v