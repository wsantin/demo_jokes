  
import time
from typing import Callable
from sqlalchemy import exc

from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute

from app.exceptions.fast_api_validation import ValidationException
from app.exceptions.fast_api_custom import CustomException

from app.database.session import SessionLocal

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
                
                return response

            
            except RequestValidationError as err:
                raise ValidationException(manual=err.errors())

            except CustomException as err:
                if hasattr(request.state, "db"):
                    request.state.db.close()
                    
                raise CustomException(status_code=err.status_code, 
                                    detail=err.detail,
                                    type=err.type,
                                    code=err.code)
            
            except Exception as err:
                print("ERROR: ",err)
                if hasattr(request.state, "db"):
                    request.state.db.close()
                    
                raise HTTPException(status_code=500, detail='Tenemos algunos inconvientes, inténtelo mas tarde')
            
            finally:
                if hasattr(request.state, "db"):
                    request.state.db.close()
                    
        return custom_route_handler