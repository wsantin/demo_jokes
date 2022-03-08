import requests

class WeatherService():
  WEATHER_API = None
  WEATHER_API_KEY = None

  def __init__(self, serviceEnv):
    self.WEATHER_API = serviceEnv.WEATHER_API
    self.WEATHER_API_KEY = serviceEnv.WEATHER_API_KEY

  def getWeatherFromPoint(self, point):
    url = str(self.WEATHER_API).format('v3','wx','forecast','hourly','2day', point, 'json', 'm','es-LA',self.WEATHER_API_KEY)

    headers= {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    return result

  def getWeatherPredictionFromPoint(self, frecuency, rangeTime, point):

    url = str(self.WEATHER_API).format('v3','wx','forecast', frecuency, rangeTime, point, 'json', 'm','es-LA',self.WEATHER_API_KEY)

    headers= {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    return result
  
  def getWeatherForecast(self, frecuency, rangeTime, point):
        
    url = str(self.WEATHER_API).format('v3','wx','forecast', frecuency, rangeTime, point, 'json', 'm','es-LA',self.WEATHER_API_KEY)
    
    headers= {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    return result