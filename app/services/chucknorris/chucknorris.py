import json
import requests

class ChucknorrisService():
  BASE_URL = None
  RENIEC_API_KEY= None

  def __init__(self, serviceEnv):
    self.BASE_URL = serviceEnv.CHUCKNORRIS_BASE_URL

  def getRandomJokes(self):
    url = '{}/jokes/random'.format(self.BASE_URL)
 
    headers= {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
    try:

      response = requests.get(url, headers=headers)
      result = response.json()
      return result
    
    except Exception as e:
      print('Error al decodificar el json {}'.format(str(e)))
      return {"error":'Error al decodificar el json {}'.format(str(e))}
