
from fastapi import Request
import base64
import json

def get_token(request: Request):
	return request.state.token

#Decoding a JWT Token
def jwt_decode(token):
	jwt_parts = token.split('.')
	jwt_parts.pop()
	jwt_data = []

	for base in jwt_parts:
		try:
			jwt_data.append(base64.b64decode(base).decode("utf-8"))
		except:
			try:
				base = base + '='
				jwt_data.append(base64.b64decode(base).decode("utf-8"))
			except:
				base = base + '=='
				jwt_data.append(base64.b64decode(base).decode("utf-8"))

	return jwt_data