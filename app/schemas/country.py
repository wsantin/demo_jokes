from datetime import datetime
from typing import Optional, Callable, Generic

from pydantic import BaseModel, EmailStr, Field, validator, UUID4, conint

class CountryCodeSchema(BaseModel):
  code: str
  description: str
  class Config:
    orm_mode = True

class CountrySchema(BaseModel):
  id: Optional[int]
  code: str
  description: str
  number_code: Optional[str]
  
  created_at: Optional[datetime]
  # updated_at: Optional[datetime]
  disabled_at: Optional[datetime]

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True

class CountryValidate(BaseModel):
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