import http
from app.exceptions.fast_status_error import error_custom

class CustomException(Exception):
    def __init__(self, status_code: int= 400, detail: str = None, type: str= 'ServerApi' ,code: str= 946) -> None:
        if detail is None:
            # detail = http.HTTPStatus(status_code).phrase
            
            if error_custom.get(status_code):            
                detail = error_custom[status_code]['detail']
            else:
                detail = 'Presentamos algunos inconvenientes. Inténtelo mas tarde'
                
        self.status_code = status_code
        self.detail = detail
        self.type = type
        self.code = code

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r},\
            type={self.type!r}, code={self.code!r})"
