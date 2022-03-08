from datetime import datetime
from typing import Optional, Callable, Generic

from enum import Enum, IntEnum
from pydantic import BaseModel, EmailStr, Field, validator, UUID4, conint

class AuthValidate(BaseModel):

  email: str = Field(..., max_length=50)
  password: str = Field(..., max_length=200)
  
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


class FruitEnum(str, Enum):
    pear = 'pear'
    banana = 'banana'



class UserValidate(BaseModel):
  telegram: Optional[str] = Field(..., min_length=2, max_length=50)
  name: str = Field(..., min_length=2, max_length=50)
  email: EmailStr = Field(...)
  password: str = Field(..., min_length=8, max_length=50)
  phone: Optional[str] = Field(None, min_length=8, max_length=15)
  code_referrer: Optional[str] = Field(None, max_length=150)
  
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

class UserActivateValidate(BaseModel):
  email: EmailStr = Field(...)
  code_activate: Optional[str] = Field(None, min_length=8, max_length=50)
  
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