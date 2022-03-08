  
import time
import base64
import json
from typing import Callable
from sqlalchemy import exc

from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute

from app.configs.environment import Config
from app.database.session import SessionLocal

from app.exceptions.fast_api_validation import ValidationException
from app.exceptions.fast_api_custom import CustomException

from app.utils.jwt import jwt_decode

class AuthDbMiddleware(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            
            ## Token
            # request_authorization = request.headers.get('Authorization', None)
            # if not request_authorization:
            #     raise CustomException(status_code=412, detail="Se requiere encabezados de autorización",
            #                     type="headers", code=995)
                
            try:
                
                ## Token decode
                # token = jwt_decode(request_authorization)[1]
                # token = json.loads(token)
                # request.state.token = token
                request.state.token = {
                    'sub':'eaa58cb4-62b5-4fe6-88b6-99b4cf14f3a3',
                    'custom:bunisse_id': '7af5d995-b281-43ee-8db7-54a2ca627be0'
                }
                
                ## Session DB
                request.state.db = SessionLocal()
                
                ## Time Response
                before = time.time()
                response: Response = await original_route_handler(request)
                duration = time.time() - before
                response.headers["X-Response-Time"] = str(duration)
                
                return response
            
            except exc.SQLAlchemyError as err:
                print("SQLAlchemyError: ",err)
                if hasattr(request.state, "db"):
                    request.state.db.close()
                    
                type_error = type(err).__name__
                if err.__dict__.get('orig', None):
                    detail_error = str(err.__dict__['orig'])
 
                    if type_error == 'IntegrityError':
                        if 'violates unique constraint' in detail_error:
                            indice_c = detail_error.index('"')
                            subcadena = str(detail_error[indice_c:].replace('"',''))
                            subcadena = subcadena.split('_')
                            variable = subcadena[1]
                            if len(subcadena) == 4  or len(subcadena) == 5:
                                variable = subcadena[1]+'_'+subcadena[2]
                            
                            # raise HTTPException(status_code=409, detail='Problemas al registrar. {} ya existe.'.format(subcadena[1]))
                            raise CustomException(status_code=422, 
                                    detail='Problemas al registrar. {} ya existe.'.format(variable),
                                    type='unique', code= variable)

                        elif 'violates not-null constraint' in detail_error:
                            indice_c = detail_error.index('"')
                            subcadena = str(detail_error[indice_c:].replace('"',''))
                            subcadena = subcadena.split(' ')

                            # raise HTTPException(status_code=409, detail='Problemas al registrar. {} no acepta espacios nulos.'.format(subcadena[0]))
                            raise CustomException(status_code=422, 
                                    detail='Problemas al registrar. {} no acepta espacios nulos.'.format(subcadena[0]),
                                    type='notnull', code= subcadena[0])

                    elif type_error == 'OperationalError':
                        raise HTTPException(status_code=504, detail='Tenemos problemas de conectividad')

                raise HTTPException(status_code=400, detail='Tenemos algunos inconvenientes')
            
            except RequestValidationError as err:
                print("RequestValidationError: ",err.errors())
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
                if hasattr(request.state, "db"):
                    request.state.db.close()
                    
                print("Exception: !: ",err)
                raise HTTPException(status_code=500, detail='Tenemos algunos inconvientes, inténtelo mas tarde')
            
            finally:
                if hasattr(request.state, "db"):
                    request.state.db.close()
                    
        return custom_route_handler