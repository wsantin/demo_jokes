from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, validator
from typing import Optional, List

class JokeRandomSchema(BaseModel):
  id: Optional[int]
  categories: List[str] = []
  icon_url: Optional[str] 
  url: Optional[str]
  created_at:  Optional[datetime]
  updated_at: Optional[datetime]

class JokeBasicSchema(BaseModel):
  id: Optional[int]
  description: Optional[str]
  created_at: Optional[datetime]
  updated_at: Optional[datetime]
  # disabled_at: Optional[datetime]

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True

class JokeValidate(BaseModel):
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
  
class JokeRandomParamValidate(BaseModel):
  path: Optional[str] = Field(None, min_length=2, max_length=150)
  
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