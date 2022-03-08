import time
import requests
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode
from exceptions.fast_api_custom import CustomException
from .utils.jwks_key import JWKSKeys

class CognitoTokenService():
  AWS_COGNITO_REGION = None
  AWS_COGNITO_USER_POOL_ID = None
  AWS_JWT_PREFIX = None
  jwksKeys = {}

  def __init__(self, serviceEnv):
    self.AWS_COGNITO_REGION = serviceEnv.AWS_COGNITO_REGION
    self.AWS_COGNITO_USER_POOL_ID = serviceEnv.AWS_COGNITO_USER_POOL_ID
    self.AWS_JWT_PREFIX = serviceEnv.AWS_JWT_PREFIX
    self.jwksKeys = JWKSKeys(serviceEnv).get_jwks_key()

  def extract_token(self, token):
    """
      Verifica si Token cuenta con Prefijo: "AGROS {TOKEN}"
    Args:
        token (string): jwt

    Raises:
        VerifyTokenException: El identificador del JWT es invalido!
        VerifyTokenException: No existe identificador del JWT!

    Returns:
        string: access_token_jwt
    """
    if ' ' in token:
      access_token_key = token.split(' ')[0]
      access_token_jwt = token.split(' ')[1]
      if access_token_key == self.AWS_JWT_PREFIX:
        return access_token_jwt
      raise CustomException(status_code=401, type='indetifier', detail='El identificador del JWT es invalido!')

    raise CustomException(status_code = 401, type='indetifier', detail='No existe identificador del JWT!')

  #Extrae Headers del Token
  def extract_headers(self, token):
    """[summary]

    Args:
        token (string): [description]

    Raises:
        VerifyTokenException: Encabezados inválido!

    Returns:
        [type]: [description]
    """
    try:
      headers = jwt.get_unverified_headers(token)
      return headers
    except JOSEError:
      raise CustomException(status_code=401, type='headers', detail='Encabezados inválido!')

  #Extrae el Jwks
  def jwk_keys(self):
    """
      jwksProject = name project: suppyseller || walkietalkie => import jwksKEYS
    """
    try:
      #Verifica Si el JWKS Lo tenemos en LOCAL
      if self.jwksKeys['keys']:
        return self.jwksKeys['keys']
      else:
        keys_url = "https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json".format(self.AWS_COGNITO_REGION,
                                                                                    self.AWS_COGNITO_USER_POOL_ID)
        response = requests.get(keys_url, timeout=30)
        response = response.json()

        return response["keys"]

    except requests.exceptions.RequestException:
      raise CustomException(status_code=401, type='validation', detail='Error validation Token')

  #Compara si Existe el Pkey del Token headers
  def find_pkey(self, headers):
    """
      jwksProject = name project: suppyseller || walkietalkie => import jwksKEYS
    """
    kid = headers["kid"]
    result = {}
    # pylint: disable=W0612
    for (i, x) in enumerate(self.jwk_keys()):
      if kid == x["kid"]:
        result = x
        break

    if result:
      return result

    raise CustomException(status_code=401, type='validation', detail='Token inválido')


  def verify_signature(self, token, pkey_data):
    """
      #Verifica si no a modificado Payload del token
      #Mediante la signature
    Args:
        token (string): jwt
        pkey_data ([type]): [description]

    Raises:
        VerifyTokenException: [description]
        VerifyTokenException: [description]
    """
    try:
      # Key data
      public_key = jwk.construct(pkey_data)
    except JOSEError:
      raise CustomException(status_code=401, type='signature', detail='Token inválido')

    #Obtiene Signature
    message, encoded_signature = str(token).rsplit(".", 1)

    # Decodifica Signature
    decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
    # Verifica Signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
      raise CustomException(status_code=401, type='signature', detail='Token a sido Modificado, Signature inválido!')

  def extract_claims(self, token):
    """
      Extraer Datos del Payload
      Args:
          token (string): [description]

      Raises:
          VerifyTokenException: Token inválido

      Returns:
          [type]: [description]
    """
    try:
      claims = jwt.get_unverified_claims(token)
      return claims
    except JOSEError:
      raise CustomException(status_code=401, type='validation', detail='Token inválido')

  def check_expiration(self, claims, current_time):
    """
      #Verifica si ya Expiro el Token
    """
    if not current_time:
      current_time = time.time()
    if current_time > claims["exp"]:
      raise CustomException(status_code=401, type='expired', detail='Token Expirado')

  def verifys(self, token, current_time=None):
    """
      #Main - Verifica todo el proceso del TOKEN
      token = JWT TOKEN JSON
      current_time = time in Seconds - Expired Token
      jwksProject = name project: suppyseller || walkietalkie => import jwksKEYS
    """

    token = self.extract_token(token)
    headers = self.extract_headers(token)
    pkey_data = self.find_pkey(headers)
    self.verify_signature(token, pkey_data)
    claims = self.extract_claims(token)
    self.check_expiration(claims, current_time)

    return claims