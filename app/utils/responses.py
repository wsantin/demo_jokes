from fastapi.responses import JSONResponse, Response 
from fastapi import status
from json import dumps

class ResponseJson(Response):
  def __init__(self, content, *args, **kwargs):
    
    status_code = kwargs.get('status_code',200)
    # print("ARGS: ",status_code)
    super().__init__(
      content=dumps({
        'status_code': status_code,
        'data': content,
        'message': 'Consulta exitosa',
      }),
      media_type="application/json",
      *args,
      **kwargs,
    )