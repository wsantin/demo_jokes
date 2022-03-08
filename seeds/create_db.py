from datetime import datetime
import sys
import os
import json
sys.path.insert(0,'./')
from sqlalchemy.orm import configure_mappers

from app.database.base import BaseQuery
from app.database.session import SessionLocal, Base, engine
from app.configs.environment import Config

from app.models.config import ConfigModel
from app.models.country import CountryModel
from app.models.gateway import GatewayModel
from app.models.user import UserModel
from app.models.message import MessageModel
from app.models.message_detail import MessageDetailModel
from app.models.cash_flow import CashFlowModel
from app.models.ticket import TicketModel

from seeds.data.user import data_users
from seeds.data.config import data_configs
from seeds.data.gateway import data_gateways
from seeds.data.country import data_countries
from seeds.data.message import data_messages
from seeds.data.message_detail import data_message_details
from seeds.data.ticket import data_tickets
from seeds.data.cash_flow import data_cash_flows

from seeds.utils.drop_cascade import drop_everything
from app.utils.encrypt import createPassword

try:

  #Create Session
  session = SessionLocal()
  
  # Drop_all Cascade
  drop_everything(session, engine)
  print("[+] Drop Model All")
  
  # Create_all Model
  Base.metadata.create_all(bind=engine)
  print("[+] Create Model All")

  # Create Configs 
  for value in data_configs:
    insert = ConfigModel.create(session,
      code = value['code'],
      description = value['description']
    )
  print("[+] Create Configs")

  # Create User 
  for value in data_users:
    insert = UserModel.create(session,
      # id = value['id'],
      name = value['name'],
      code_affiliate = value['code_affiliate'],
      telegram = value['telegram'],
      email = value['email'],
      password = createPassword(value['email'], value['password']),
      phone = value['phone'],
      sender_default = value['sender_default'],
      api_key = value['api_key'],
      api_secret = value['api_secret'],
      nivel = value['nivel'],
      status = value['status'],
      observation = value['observation']
    )
  print("[+] Create Users")

  # Create Gateways 
  for value in data_gateways:
    insert = GatewayModel.create(session,
      # id = value['id'],
      code = value['code'],
      description = value['description'],
      description_admin = value['description_admin']
    )
  print("[+] Create Gateways")

  # Create Tickets 
  for value in data_tickets:
    insert = TicketModel.create(session,
      # id = value['id'],
      code = value['code'],
      user_id = value['user_id'],
      reply = value['reply'],
      subject = value['subject'],
      message = value['message'],
      parent_id = value['parent_id']
    )
  print("[+] Create Tickets")

  # Create Countries 
  for value in data_countries:
    disabled_at = None 
    if( value.get('status') and value.get('status') == True):
      disabled_at = datetime.now()
    insert = CountryModel.create(session,
      # id = value['id'],
      code = value['code'],
      description = value['description'],
      number_code = value.get('number_code') or None,
      disabled_at = disabled_at
    )
  print("[+] Create Countries")

  
  # Create Messages 
  for value in data_messages:
    insert = MessageModel.create(session,
      # id = value['id'],
      user_id = value['user_id'],
      gateway_id = value['gateway_id'],
      sender = value['sender'],
      message = value['message'],
      type = value['type'],
      status = value['status'],
      # description = value['description'],
      schedule_date = value.get('schedule_date') or None,
      ip = value['ip'],
      sent_from = value['sent_from']
    )
  print("[+] Create Messages")

  # Create Messages Details
  for value in data_message_details:
    insert = MessageDetailModel.create(session,
      # id = value['id'],
      message_id = value['message_id'],
      country_id = value['country_id'],
      phone = value['phone'],
      sent_at = value['sent_at'],
      readed_at = value['readed_at'],
      status = value['status'],
      price = value['price'],
      price_real = value['price_real'],
      description = value.get('description') or None,
      description_admin = value['description_admin']
    )
  print("[+] Create Messages Details")
 
  
  
  
  # Create CashFlowModel
  for value in data_cash_flows:
    insert = CashFlowModel.create(session,
      # id = value['id'],
      code = value.get('code') or None,
      user_id = value.get('user_id') or None,
      service = value.get('service') or None,
      credit_amount = value.get('credit_amount') or None,
      output_amount = value.get('output_amount') or None,
      motive = value.get('motive') or None,
      credit_total = value.get('credit_total') or None,
      status = value.get('status') or None,
      observation = value.get('observation') or None,
      reference_user_id = value.get('reference_user_id') or None,
      approved_user_id = value.get('approved_user_id') or None
    )
  
  print("[+] Create CashFlowModel")

  session.commit()
  configure_mappers()
except Exception as error:
  print("Error: ",error)

