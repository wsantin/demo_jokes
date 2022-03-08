
from datetime import datetime
from typing import Optional, List, Any, Generic, TypeVar

from pydantic import BaseModel, EmailStr, Field, validator, UUID4
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')

class PaginationsBase(GenericModel, Generic[DataT]):
    # description: Optional[str] = None
    # next_num: Optional[int] = None
    page: int = 1
    per_page: int = 10
    total: int 
    items: Optional[DataT] = []
    
    class Config:
        orm_mode = True

class paginationsValidate(BaseModel):
    page:str = Field(1, max_length=10)
    per_page: str = Field(10, max_length=20)
    sort_by: Optional[str] = Field('', max_length=20)
    order: Optional[str] = Field('', max_length=4)
    search: Optional[str] = Field('', max_length=50)
