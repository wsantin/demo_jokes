import jwt
from datetime import timezone, datetime ,timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from starlette.endpoints import HTTPEndpoint

from app.configs.environment import Config
from app.database.get_db import get_db
from app.utils.jwt import get_token

from app.exceptions.fast_api_custom import CustomException

from app.models.user import UserModel
from app.models.config import ConfigModel
from app.schemas import response, user, auth, pagination
from app.services.smtp.smtp import SmtpService
from app.utils.encrypt import createPassword, comparePassword
from app.utils.random import random_string, random_string_number, random_number

smtp_service = SmtpService(Config)

class AuthSignipResource(HTTPEndpoint):
  @staticmethod
  async def post( body: auth.AuthValidate, db: Session = Depends(get_db) ):
    email = body.email
    password = body.password

    query_user = UserModel.read_by_email(email)
    if not query_user:
      raise CustomException(status_code=404, type='NoData', code="access_invalid")

    if query_user.status == 'desactivate':
      raise CustomException(status_code=401, code="desactivate")
    
    if query_user.status == 'desactivate_bot':
      raise CustomException(status_code=401, code="desactivate_bot")

    if query_user.status == 'code':
      
      # if query_user.aproved_expire_at < datetime.now():
      #   raise CustomException(status_code=409, code="code_expired_activate")

      if query_user.nivel !='admin' and query_user.aproved_qty >=6 :
        raise CustomException(status_code=409, code="limit_exceeded_code_activate")

      #GENERATE CODE ACTIVATE
      aproved_code = random_number(6)
      print("aproved_code: ",aproved_code)
      # aproved_expire_at = datetime.now(timezone.utc) + timedelta(minutes=1)
      aproved_expire_at = datetime.now() + timedelta(minutes=1)

      query_user.aproved_code = aproved_code
      query_user.aproved_expire_at = aproved_expire_at
      query_user.aproved_qty = query_user.aproved_qty + 1

      db.flush()

      #SEND EMAIL SMTP
      smtp_service.sent_aproved_code(query_user.name, aproved_code, query_user.email)

      db.commit()
      raise CustomException(status_code=409, code="required_code_activate")

    compare = comparePassword(query_user.password, email, password)
    if(compare == False):
      raise CustomException(status_code=404, type='NoData', code="access_invalid")
    
    payload= {
      # "date": str(datetime.now(timezone.utc) ),
      "date": str(datetime.now() ),
      "code_affiliate": query_user.code_affiliate,
      "name": query_user.name,
      "email": query_user.email,
      "phone": query_user.phone,
      "nivel": query_user.nivel
    }

    encoded_jwt = jwt.encode({"payload": payload}, Config.JWT_SECRET, algorithm="HS256")

    return encoded_jwt

class AuthSignupResource(HTTPEndpoint):
  @staticmethod
  async def post( body: auth.UserValidate, db: Session = Depends(get_db) ):
    code_referrer = None
    if(body.code_referrer):
      query_referrer = UserModel.read_by_code_affiliate(body.code_referrer);
      if not query_referrer:
        raise CustomException(status_code=404, type='NoData', code="not_found_referrer")
      code_referrer = query_referrer.id 

    email = body.email
    password = body.password
    password_encrypt = createPassword(email, password)
    telegram = body.telegram
    name = body.name
    
    query_email = UserModel.read_by_email(email);
    if query_email:
      raise CustomException(status_code=500, code="error")

    code_affiliate = random_string(8, 'lowercase')
    sender_default = ConfigModel.read_by_code('sender').description or 'InfoBipp'

    api_key = random_string_number(30)
    api_secret = random_string_number(10)

    # status = ConfigModel.read_by_code('user_register_approved').description or 'code'
    status = 'code'

    #GENERATE CODE ACTIVATE
    aproved_code = random_number(6)
    # aproved_expire_at = datetime.now(timezone.utc) + timedelta(minutes=1)
    aproved_expire_at = datetime.now() + timedelta(minutes=1)
  
    query_user = UserModel.create(db, 
        code_affiliate= code_affiliate, 
        name = name,
        telegram=telegram, 
        email= email, 
        password=password_encrypt, 
        phone=body.phone, 
        sender_default= sender_default,
        api_key = api_key,
        api_secret = api_secret,
        status = status,
        aproved_code = aproved_code,
        aproved_expire_at = aproved_expire_at,
        referrer_user_id = code_referrer
    )
    db.commit()

    #SEND EMAIL SMTP
    smtp_service.sent_aproved_code(query_user.name, aproved_code, query_user.email)

    return status

class RecoveryByEmailResource(HTTPEndpoint):
  @staticmethod
  async def put(email: str, db: Session = Depends(get_db)):
    query_user = UserModel.read_by_email(email)
    if not query_user:
      raise CustomException(status_code=404, type='NoData', code="not_fount")

    #GENERATE CODE ACTIVATE
    aproved_code = random_number(6)
    aproved_expire_at = datetime.now() + timedelta(minutes=1)

    query_user.aproved_code = aproved_code
    query_user.aproved_expire_at = aproved_expire_at
    query_user.aproved_qty = query_user.aproved_qty + 1

    #SEND EMAIL SMTP
    smtp_service.sent_aproved_code(query_user.name, aproved_code, query_user.email)
    db.commit() 
    return 

class ActivateUserResource(HTTPEndpoint):
  @staticmethod
  async def put(body: auth.UserActivateValidate, db: Session = Depends(get_db)):
    email = body.email
    code_activate = body.code_activate
    print("BOYD: ",body)
    
    now = datetime.now()
    query_user = UserModel.read_by_email(email)
    if not query_user:
      return

    if query_user.status == 'aproved':
      raise CustomException(status_code=403, code="user_aproved")

    print("query_user.aproved_expire_at: ",query_user.aproved_expire_at)

    if query_user.aproved_qty >=6 and query_user.aproved_expire_at < now:
      query_user.aproved_qty = 0
      query_user.aproved_expire_at = None

    if query_user.nivel !='admin' and query_user.aproved_qty >=6 and query_user.aproved_expire_at >= now:
      raise CustomException(status_code=403, code="limit_exceeded_code_activate:10")

    if not code_activate:
      
       #GENERATE CODE ACTIVATE
      aproved_code = random_number(6)
      aproved_expire_at = now + timedelta(minutes=1)
      aproved_reload_at = now + timedelta(minutes=10)
      # aproved_reload_at = now + timedelta(seconds=30)
      
      query_user.aproved_code = aproved_code
      query_user.aproved_expire_at = aproved_expire_at
      query_user.aproved_qty = query_user.aproved_qty + 1
      
      if not query_user.aproved_reload_at:
        query_user.aproved_reload_at = aproved_reload_at

      #SEND EMAIL SMTP
      smtp_service.sent_aproved_code(query_user.name, aproved_code, query_user.email)
      db.commit() 

      return 

    if query_user.aproved_expire_at < now:
      raise CustomException(status_code=409, code="code_expired_activate")
    
    if query_user.aproved_code != body.code_activate:
      raise CustomException(status_code=409, code="code_invalid_activate")

    
      
    user_register_approved = ConfigModel.read_by_code('user_register_approved').description or 'code'
    if user_register_approved == 'aproved':
      query_user.status = 'aproved'
    else:
      query_user.status = 'pending'

    query_user.aproved_code = 0
    query_user.aproved_qty = 0
    query_user.aproved_expire_at = None

    db.commit() 
    return query_user.status

  