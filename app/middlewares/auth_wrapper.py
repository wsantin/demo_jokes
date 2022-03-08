from functools import wraps
from fastapi import Request, HTTPException, Header

def auth_required(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        # request_authorization = request.headers.get('Authorization')
        print("REQUEST: ",Header)
        # if not request_authorization: 
        #     raise HTTPException(status_code=401, detail="headers Error")
        
        return await handler(*args, **kwargs)
    return wrapper

# def auth_required(handler):
#     async def wrapper(request: Request, *args, **kwargs):
#         request_authorization = request.headers.get('Authorization')
#         if not request_authorization: 
#             raise HTTPException(status_code=401, detail="headers Error")
        
#         return await handler(*args, **kwargs)

#     # Fix signature of wrapper
#     import inspect
#     wrapper.__signature__ = inspect.Signature(
#         parameters = [
#             # Use all parameters from handler
#             *inspect.signature(handler).parameters.values(),

#             # Skip *args and **kwargs from wrapper parameters:
#             *filter(
#                 lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
#                 inspect.signature(wrapper).parameters.values()
#             )
#         ],
#         return_annotation = inspect.signature(handler).return_annotation,
#     )

#     return wrapper