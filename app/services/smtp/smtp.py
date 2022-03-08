from datetime import datetime
import os, smtplib, ssl
from app.exceptions.fast_api_custom import CustomException

class SmtpService():
  SMTP_URL = None
  SMTP_PORT = None
  SMTP_USER = None
  SMTP_PASSWORD= None

  def __init__(self, serviceEnv):
    self.SMTP_URL = serviceEnv.SMTP_URL
    self.SMTP_PORT = serviceEnv.SMTP_PORT
    self.SMTP_USER = serviceEnv.SMTP_USER
    self.SMTP_PASSWORD = serviceEnv.SMTP_PASSWORD
    self.MESSAGE_CODE = "Hi {name},Code Activate: {aproved_code}"

  def get_login(self):
    """Conextion Smtp"""
    context = ssl.create_default_context()
    # server = smtplib.SMTP(self.SMTP_URL, self.SMTP_PORT, context=context)
    server = smtplib.SMTP(self.SMTP_URL, self.SMTP_PORT)
    server.ehlo()
    server.starttls()

    try:
      print("SMTP_USER: ",self.SMTP_USER)
      print("SMTP_PASSWORD: ",self.SMTP_PASSWORD)
      server.login(self.SMTP_USER, self.SMTP_PASSWORD)
      return server
    except smtplib.SMTPAuthenticationError as err:
      print("STML: ", err)
      raise CustomException(status_code=500, code="connect_smtp")

  def sent_aproved_code(self, name, aproved_code, to_addrs, subject=None):
      """Crea una nueva coleccion de elementos

      Args:
          tableName (string): El nombre de la tabla
          item (dict): La coleccion de elementos

      Returns:
          boolean: Verdadero si fue exitoso y falso si hubo error
      """
      server = self.get_login()
      try:
        print("server: ",server)
        if not subject:
          subject= "Activate User"

        # print("name: ",name)
        # print("aproved_code: ",aproved_code)
        # print("MESSAGE_CODE: ",self.MESSAGE_CODE)
        body = str(self.MESSAGE_CODE).replace("{name}", name)
        body = body.replace("{aproved_code}", aproved_code)
        # print("body: ",body)
        
        server.sendmail(from_addr=self.SMTP_USER, to_addrs=to_addrs, msg=f'Subject: {subject}\n\n {body}')
        server.close()
      except smtplib.SMTPAuthenticationError as err:
        print("STML: ", err)
        raise CustomException(status_code=500, code="sent_message")