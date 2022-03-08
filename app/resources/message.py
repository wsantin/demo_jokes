from app.models.gateway import GatewayModel
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import func, case, literal_column
from sqlalchemy.orm import Session
from starlette.endpoints import HTTPEndpoint

from app.database.get_db import get_db
from app.utils.jwt import get_token

from app.exceptions.fast_api_custom import CustomException

from app.models.user import UserModel
from app.models.cash_flow import CashFlowModel
from app.models.message import MessageModel
from app.models.message_detail import MessageDetailModel
from app.schemas import response, user, message, user_detail, pagination

class MessagesResource(HTTPEndpoint):
  @staticmethod
  async def get(params: pagination.paginationsValidate = Depends(), 
                db: Session = Depends(get_db), token = Depends(get_token) ):

    query  = db.query(MessageModel.id, MessageModel.type, MessageModel.sender, \
              MessageModel.status, MessageModel.ip, MessageModel.sent_from,\
              MessageModel.created_at, UserModel.name.label('user_name'),\
              func.count(MessageDetailModel.id).label('message_detail_total'),\
              func.sum(case((MessageDetailModel.status == 'schedule', 1), else_=0)).label('message_detail_queue'),\
              func.sum(case(( MessageDetailModel.status.in_(['create', 'in_process']), 1 ), else_= 0)).label('message_detail_in_proccess'),\
              func.sum(case((MessageDetailModel.status == 'sent', 1), else_=0)).label('message_detail_success'),\
              func.sum(case((MessageDetailModel.status == 'failed', 1), else_=0)).label('message_detail_failed'),\
              func.sum(case((MessageDetailModel.status == 'canceled', 1), else_=0)).label('message_detail_canceled'),\
              GatewayModel.description.label('gateway_name'),\
              MessageModel.message
              )\
            .join(UserModel, UserModel.id == MessageModel.user_id)\
            .join(MessageDetailModel, MessageDetailModel.message_id == MessageModel.id)\
            .join(GatewayModel, GatewayModel.id == MessageModel.gateway_id)\
            .group_by(MessageModel.id, MessageModel.type, MessageModel.sender, MessageModel.status, \
              MessageModel.ip, MessageModel.sent_from, MessageModel.created_at, GatewayModel.description)

    query_fin = MessageModel.read_paginate(query, params)
    return pagination.PaginationsBase(
      total=query_fin.total, page=query_fin.page, per_page=query_fin.per_page, items=query_fin.items
    )

  @staticmethod
  async def post( body: user.UserValidate, db: Session = Depends(get_db), token = Depends(get_token) ):
    query_user = MessageModel.create(db, last_name=body.last_name, first_name= body.first_name, phone=body.phone, 
                                  description=body.description)
    db.commit()
    return query_user.id

class MessageResource(HTTPEndpoint):
  @staticmethod
  async def get(message_id: int, db: Session = Depends(get_db), token = Depends(get_token)):
    # query_user = MessageModel.read(message_id)
    query_user = MessageModel.query.filter_by(id=message_id).first()
      #.join(CashFlowModel, CashFlowModel.message_id == MessageModel.id, isouter=True)
    if not query_user:
      raise CustomException(status_code=404, type='NoData',  detail="No existe Usuario")
    print("query_user: ",query_user)
    # query_message = MessageModel.read_by_message_id(query_user.id)
    # query_transation = CashFlowModel.read_by_message_id(query_user.id)
    # print("query_user: ",query_user)
    # print("query_user: ",query_user.cash_flow)
    # # return user.Transationschema(query_user,
    # #   prueba=1
    # # )
    return query_user
  
  @staticmethod
  async def put(message_id: int, body: user.UserValidate, db: Session = Depends(get_db), token = Depends(get_token)):
    query_user = MessageModel.update(db, str(message_id), last_name=body.last_name, first_name= body.first_name, phone=body.phone,
                                    description=body.description)
    db.commit()
    return
  
  @staticmethod
  async def delete(message_id: int, db: Session = Depends(get_db), token = Depends(get_token)):
    query_user = MessageModel.delete(db, message_id)
    db.commit()
    return 

class MessageDetailsResource(HTTPEndpoint):
  @staticmethod
  async def get(message_id: int, db: Session = Depends(get_db), token = Depends(get_token) ):
    query = MessageDetailModel.read_all_by_message_id(message_id)
    return query


  