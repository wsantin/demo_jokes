
from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel, EmailStr, Field, validator

class ResponseSchema(BaseModel):
    message: Optional[str] = 'Consulta con exito'
    data: Optional[Any]
    status_code: Optional[int] = 200
    