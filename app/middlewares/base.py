  
import time
from typing import Callable
from sqlalchemy import exc

from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute

from exceptions.fast_api_validation import ValidationException
from exceptions.fast_api_custom import CustomException

class BaseMiddleware(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                
                ## Time Response
                before = time.time()
                response: Response = await original_route_handler(request)
                duration = time.time() - before
                response.headers["X-Response-Time"] = str(duration)
                # response.token= 'TOKENasasa'
                
                return response

            except RequestValidationError as err:
                # body = await request.body()
                # detail = {"errors": err.errors(), "body": body.decode()}
                raise ValidationException(manual=err.errors())

            except CustomException as err:
                raise CustomException(status_code=err.status_code, 
                                    detail=err.detail,
                                    type=err.type,
                                    code=err.code)
            
            except Exception as err:
                print("Error: !: ",err)
                raise HTTPException(status_code=500, detail='Tenemos algunos inconvientes, inténtelo mas tarde')
            
            finally:
                request.state.db.close()
        return custom_route_handler