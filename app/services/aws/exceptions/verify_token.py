class VerifyTokenException(Exception):
  def __init__(self, message, code='auth', status_code='401'):
    """
      Exepcion cuando el codigo de verificación no coincide.
    """
    Exception.__init__(self)
    self.message = message
    self.code = code
    self.status_code = status_code
