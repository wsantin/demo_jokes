from datetime import datetime
from typing import Optional, Callable, Generic, List

from pydantic import BaseModel, EmailStr, Field, validator, UUID4, conint


class UserNameSchema(BaseModel):
  name: Optional[str]

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True


class UserBasicSchema(BaseModel):
  id: Optional[int]
  # code_affiliate: Optional[str]
  telegram: Optional[str]
  name: str
  email: str
  nivel: str
  status: str
  created_at: Optional[datetime]
  updated_at: Optional[datetime]
  # disabled_at: Optional[datetime]

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True

class UserSchema(BaseModel):
  id: Optional[int]
  code_affiliate: Optional[str]
  telegram: Optional[str]
  name: str
  email: str
  # password: str
  phone: str
  sender_default: Optional[str]
  api_key: Optional[str]
  api_secret: Optional[str]
  nivel: str
  status: str
  aproved_code: Optional[str]
  aproved_expire_at: Optional[datetime]
  aproved_qty: Optional[int]
  attempts_allowed_qty: Optional[int]
  attempts_allowed_date: Optional[datetime]
  observation: Optional[str]

  created_at: Optional[datetime]
  updated_at: Optional[datetime]
  # disabled_at: Optional[datetime]

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True

class UserValidate(BaseModel):
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