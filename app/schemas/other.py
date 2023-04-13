from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, validator
from typing import Annotated, Optional, List

class McmParamValidate(BaseModel):
  number: str
  
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
  
class IncrementParamValidate(BaseModel):
  number: int
  
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