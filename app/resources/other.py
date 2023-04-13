from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.endpoints import HTTPEndpoint
from typing import Optional, List

from app.exceptions.fast_api_custom import CustomException

from app.configs.environment import Config
from app.schemas import other

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def lcm(numbers: List[int]) -> int:
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = result * numbers[i] // gcd(result, numbers[i])
    return result


class McmResource(HTTPEndpoint):
  @staticmethod
  async def get(params: other.McmParamValidate = Depends()):
    number_new = []
    list_number = params.number.split(',')
    for s in list_number:
        int(s)
        if not s.isdigit():
            raise CustomException(status_code=409, code="1221", type='validateError', detail="No es un numero entero")
        else:
            number_new.append(int(s))
    return lcm(number_new)
  

class IncrementResource(HTTPEndpoint):
  @staticmethod
  async def get(params: other.IncrementParamValidate = Depends()):
    print("params: ",params)
    return params.number + 1
