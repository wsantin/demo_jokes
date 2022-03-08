import http
from app.exceptions.fast_status_error import error_custom

class ValidationException(Exception):
  def __init__(self, manual: int= None) -> None:
    self.manual = manual

  def __repr__(self) -> str:
    class_name = self.__class__.__name__
    return f"{class_name}(manual={self.manual!r})"
