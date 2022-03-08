from twilio.rest import Client

class TwilioService():
  TWILIO_ACCOUNT_SID = None
  TWILIO_ACCOUNT_TOKEN = None
  TWILIO_FROM_WSP = None
  TWILIO_FROM_SMS = None
  TWILIO_FROM_CALL = None

  def __init__(self, serviceEnv):
    self.TWILIO_ACCOUNT_SID = serviceEnv.TWILIO_ACCOUNT_SID
    self.TWILIO_ACCOUNT_TOKEN = serviceEnv.TWILIO_ACCOUNT_TOKEN
    self.TWILIO_FROM_WSP = serviceEnv.TWILIO_FROM_WSP
    self.TWILIO_FROM_SMS = serviceEnv.TWILIO_FROM_SMS
    self.TWILIO_FROM_CALL = serviceEnv.TWILIO_FROM_CALL
    
  def client(self):
    return Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_ACCOUNT_TOKEN)

  def send_whatsapp(self, phone, message='',status_callback=None):
    return self.client().messages.create(
      from_=self.TWILIO_FROM_WSP,
      to='whatsapp:'+phone,
      body= message,
      status_callback=status_callback
    )

  def send_sms(self, phone='', message=''):
    return self.client().messages.create(
      from_= self.TWILIO_FROM_SMS,
      to= phone,
      body= message
    )
    
  def response_message(self, resp, body=False ,media=False):

    msg = resp.message()
    if media:
        msg.media(media)
    if body:
        msg.body(body)
    return str(resp)

  def send_call(self, url, phone, status_callback=None):
    return self.client().calls.create(
        url=url,
        to=phone,
        from_= self.TWILIO_FROM_CALL,
        status_callback=status_callback,
        status_callback_event=['answered', 'completed', 'ringing'],
    )