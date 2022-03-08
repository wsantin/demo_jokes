from datetime import datetime
from typing import Optional, Callable, Generic

from pydantic import BaseModel, EmailStr, Field, validator, UUID4, conint
from app.schemas.user import UserNameSchema

class CashFlowPaginationSchema(BaseModel):
  id: Optional[int]
  code: str
  # user_id: int
  service: Optional[str]
  credit_amount: Optional[float]
  output_amount: Optional[float]
  motive: str
  credit_total: float
  status: str
  observation: Optional[int]

  user: Optional[UserNameSchema] = None

  created_at: Optional[datetime]
  updated_at: Optional[datetime]
  # disabled_at: Optional[datetime]

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True

class CashFlowSchema(BaseModel):
  id: Optional[int]
  code: str
  # user_id: int
  service: Optional[str]
  credit_amount: Optional[float]
  output_amount: Optional[float]
  motive: str
  credit_total: float
  status: str
  observation: Optional[int]

  created_at: Optional[datetime]
  updated_at: Optional[datetime]
  # disabled_at: Optional[datetime]

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True

class CashFlowValidate(BaseModel):
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