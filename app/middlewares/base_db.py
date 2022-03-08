  
import time
from typing import Callable
from sqlalchemy import exc

from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute

from app.exceptions.fast_api_validation import ValidationException
from app.exceptions.fast_api_custom import CustomException

from app.database.session import SessionLocal

class BaseDbMiddleware(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                
                ## Session DB
                request.state.db = SessionLocal()
                
                ## Time Response
                before = time.time()
                response: Response = await original_route_handler(request)
                duration = time.time() - before
                response.headers["X-Response-Time"] = str(duration)
                # response.token= 'TOKENasasa'
                
                return response
            
            except exc.SQLAlchemyError as err:
                if hasattr(request.state, "db"):
                    request.state.db.close()
                    
                type_error = type(err).__name__
                detail_error = str(err.__dict__['orig'])
 
                if type_error == 'IntegrityError':
                    if 'violates unique constraint' in detail_error:
                        indice_c = detail_error.index('"')
                        subcadena = str(detail_error[indice_c:].replace('"',''))
                        subcadena = subcadena.split('_')
                        raise HTTPException(status_code=409, detail='Problemas al registrar cultivo. {} ya existe.'.format(subcadena[1]))
                
                elif type_error == 'OperationalError':
                    raise HTTPException(status_code=504, detail='Tenemos problemas de conectividad')

                raise HTTPException(status_code=400, detail='Tenemos algunos inconvenientes')
            
            except RequestValidationError as err:
                if hasattr(request.state, "db"):
                    request.state.db.close()
                # body = await request.body()
                # detail = {"errors": err.errors(), "body": body.decode()}
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