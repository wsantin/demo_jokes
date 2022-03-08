from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.fast_status_error import error_custom

# Aqui entra error de FastApi y SqlAlchemy
async def http_exception_handler(request: Request, exception):
    
    # return JSONResponse(
    #         status_code = 422,
    #         content = {
    #             "error": "fd",
    #             "message": "Validación de parametros incorrecto", 
    #             "type": "ValidateFields", 
    #             "code": 190,
    #             "status_code": 422
    #         }
    #     )
    
    try:
        status_code = exception.status_code
    except Exception:
      status_code = 500
    
    try:
        detail = exception.detail
    except Exception:
        if error_custom.get(status_code):            
            detail = error_custom[status_code]['detail']
        else:
            detail = 'Presentamos algunos inconvenientes. Inténtelo mas tarde'
            
    return JSONResponse(
            status_code = status_code,
            content = {
                "error": {
                    "message": detail,
                    "code": 1546,             
                    #"error_subcode": 460, #Sub code manejarlo por Error de autenticación
                },
                "type": "ServerApi", 
                "status_code": status_code
            }
        )

async def http_exception_handler_custom(request: Request, exception):
    
    detail = exception.detail
    status_code = exception.status_code
    type = exception.type
    code = exception.code

    return JSONResponse(
            status_code = status_code,
            content = {
                "error": {
                    "message": detail,
                    "code": code,
                    #"error_subcode": 460, #Sub code manejarlo por Error de autenticación
                },
                "type": type,
                "status_code": status_code
            }
        )

async def validation_exception_handler(request: Request, exception):
    
    try:
        errors = exception.errors()
    except Exception as ex:
        errors =  exception.manual
        
    try:
        # errors = exception.errors()
        fields_error= {}
        for value in list(errors):
            types = value['type'].split('.')
            msg = value['msg']
            fields = list(value['loc'])[1]
            if len(types) > 1:
                type_value = types[1]
                # print("type_value: ",type_value)
                if type_value == 'jsondecode':
                    return JSONResponse(
                        status_code = 422,
                        content = {
                            "error": {
                                #"error_subcode": 460, #Sub code manejarlo por Error de autenticación
                            },
                            "message": "Validación Json incorrecto", 
                            "type": "ValidateFields", 
                            "code": 189,
                            "status_code": 422
                        }
                    )
                    # errors_finals.append({"type":type_value,"detail":"Caracter inválido", "field": fields})
                elif type_value == 'email':
                    fields_error.update({fields:"Email no es correcto"})
                elif type_value == 'date':
                    fields_error.update({fields:"La fecha es incorrecta"})
                elif type_value == 'uuid':
                    fields_error.update({fields:"El valor no es un UUID"})
                elif type_value == 'integer':
                    fields_error.update({fields:"El valor no es un entero válido"})
                elif type_value == 'float':
                    fields_error.update({fields:"El valor no es decimal"})
                elif type_value == 'bool':
                    fields_error.update({fields:"El valor no es un booleano"})
                elif type_value == 'json':
                    fields_error.update({fields:"Json inválido"})
                elif type_value == 'list':
                    fields_error.update({fields:"Lista inválido"})
                elif type_value == 'none':
                    fields_error.update({fields:"Campo requerido"})
                elif type_value == 'missing':
                    fields_error.update({fields:"Campo requerido"})
                elif type_value == 'any_str':
                    character_max = [int(s) for s in msg.split() if s.isdigit()][0]
                    if types[2]== 'min_length':
                        fields_error.update({fields:f"Asegúrese de que este valor tenga como minimo {character_max} caracteres"})
                    elif types[2]== 'max_length':
                        fields_error.update({fields:f"Asegúrese de que este valor tenga como máximo {character_max} caracteres"})
                    else:
                        fields_error.update({fields:"Asegúrese de que este valor cumpla los carácteres permitidos"})
                else:
                    fields_error.update({fields:"Asegúrese de que este valor cumpla los carácteres permitidos"})
            else:
                type_value = types[0]
                fields_error.update({fields:"El valor no es correcto"})
            
        return JSONResponse(
            status_code = 422,
            content = {
                "errors": fields_error,
                "message": "Validación de parametros incorrecto", 
                "type": "ValidateFields", 
                "code": 190,
                "status_code": 422
            }
        )
        
    except Exception as ex:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "message": "Validación", 
                    #"error_subcode": 460, #Sub code manejarlo por Error de autenticación
                },
                "type": "ValidateFields", 
                "code": 191,
                "status_code": 422
            }
        )
    