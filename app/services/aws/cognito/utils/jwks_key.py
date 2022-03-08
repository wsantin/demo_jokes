import json

class JWKSKeys():
  envKeys = None
  def __init__(self, envKeys):
    self.envKeys =envKeys

  def get_jwks_key(self):
    return {
      "keys": [
        {
          "alg":  json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY1).get('alg'),
          "e": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY1).get('e'),
          "kid": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY1).get('kid'),
          "kty": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY1).get('kty'),
          "n": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY1).get('n'),
          "use": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY1).get('use'),
        },
        {
          "alg": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY2).get('alg'),
          "e": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY2).get('e'),
          "kid": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY2).get('kid'),
          "kty": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY2).get('kty'),
          "n": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY2).get('n'),
          "use": json.loads(self.envKeys.AWS_COGNITO_JWKS_KEY2).get('use'),
        }
      ]
    }
