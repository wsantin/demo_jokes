from datetime import datetime
from typing import Optional, Callable, Generic

from pydantic import BaseModel, EmailStr, Field, validator, UUID4, conint

from app.schemas.gateway import GatewayBasicAdminSchema
from app.schemas.user import UserNameSchema

class MessagePaginationSchema(BaseModel):
  id: Optional[int]
  # user_id: int
  # gateway_id: int
  sender: str
  # message: Optional[str]
  type: Optional[str]
  status: str
  schedule_date: Optional[datetime]
  ip: Optional[str]
  sent_from: Optional[str]
  user_name: str
  message_detail_total: Optional[int] = 0
  message_detail_queue: Optional[int] = 0
  message_detail_in_proccess: Optional[int] = 0
  message_detail_success: Optional[int] = 0
  message_detail_failed: Optional[int] = 0
  message_detail_canceled: Optional[int] = 0
  gateway_name: Optional[str]
  message: Optional[str]
  # gateway: Optional[GatewayBasicAdminSchema] = None
  # user: Optional[UserNameSchema] = None

  created_at: Optional[datetime]
  # updated_at: Optional[datetime]
  disabled_at: Optional[datetime]

  class Config:
    # orm_mode = True
    arbitrary_types_allowed = True

class MessageSchema(BaseModel):
  id: Optional[int]
  # user_id: int
  # gateway_id: int
  sender: str
  message: Optional[str]
  type: str
  status: str
  schedule_date: Optional[datetime]
  ip: Optional[str]
  sent_from: Optional[str]

  gateway: Optional[GatewayBasicAdminSchema] = None

  created_at: Optional[datetime]
  # updated_at: Optional[datetime]
  disabled_at: Optional[datetime]

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True

class MessageValidate(BaseModel):
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