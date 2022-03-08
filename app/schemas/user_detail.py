from datetime import datetime
from typing import Optional, Callable, Generic, List

from pydantic import BaseModel, EmailStr, Field, validator, UUID4, conint

from app.schemas.message import MessageSchema
from app.schemas.cash_flow import CashFlowSchema

class UserDetailBasicSchema(BaseModel):
  user_id: Optional[str]
  messages: List[MessageSchema] = None
  transations: List[CashFlowSchema] = None
  current_balance: Optional[float] = None
  last_recharge: Optional[float] = None

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True
