import http.client
import json
from base64 import b64encode

class InfobipService():
  INFOBIP_AUTH_HASH = None
  INFOBIP_API = None
  HOST_API = None

  def __init__(self, serviceEnv):
    self.INFOBIP_AUTH_HASH = serviceEnv.INFOBIP_AUTH_HASH
    self.INFOBIP_API = serviceEnv.INFOBIP_API
    self.HOST_API = serviceEnv.HOST_API


  def send_sms(self, msg, phone, endPointRelative):
    auth_hash = b64encode('{}'.format(self.INFOBIP_AUTH_HASH).encode()).decode('UTF-8')
    conn = http.client.HTTPSConnection(self.INFOBIP_API)
    authorization = 'Basic {}'.format(auth_hash)
    ENDPOINT_SMS = "/sms/2/text/advanced"
    payload_dict = {
      "messages":[
        {
          "from": "AgrosDev",
          "destinations": [{
              "to":phone
            }
          ],
          "text": msg,
          "notifyContentType": "application/json"
        }
      ]
    }
    if not endPointRelative is None:
      payload_dict = {
        "messages":[
          {
            "from": "AgrosDev",
            "destinations": [{
                "to":phone
              }
            ],
            "text": msg,
            "notifyUrl": self.HOST_API + endPointRelative,
            "notifyContentType": "application/json"
          }
        ]
      }

    payload = json.dumps(payload_dict)

    headers = {
        'Authorization': authorization,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    conn.request("POST", ENDPOINT_SMS, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print('data de infobip', data)
    return data
