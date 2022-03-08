from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from starlette.endpoints import HTTPEndpoint

from app.database.get_db import get_db
from app.utils.jwt import get_token

from app.exceptions.fast_api_custom import CustomException

from app.models.user import UserModel
from app.models.cash_flow import CashFlowModel
from app.models.message import MessageModel
from app.schemas import response, user, message, user_detail, pagination

class UsersCustomersResource(HTTPEndpoint):
  @staticmethod
  async def get(params: pagination.paginationsValidate = Depends(), 
                db: Session = Depends(get_db), token = Depends(get_token) ):
    print("params: ",params)
    query = UserModel.read_paginate(params, 'customer')
    print("query: ",query)
    return pagination.PaginationsBase(
      total=query.total, page=query.page, per_page=query.per_page, items=query.items
    )

  @staticmethod
  async def post( body: user.UserValidate, db: Session = Depends(get_db), token = Depends(get_token) ):
    query_user = UserModel.create(db, last_name=body.last_name, first_name= body.first_name, phone=body.phone, 
                                  description=body.description)
    db.commit()
    return query_user.id

class UsersOperatorsResource(HTTPEndpoint):
  @staticmethod
  async def get(params: pagination.paginationsValidate = Depends(), 
                db: Session = Depends(get_db), token = Depends(get_token) ):
    print("params: ",params)
    query = UserModel.read_paginate(params, 'operador')
    print("query: ",query)
    return pagination.PaginationsBase(
      total=query.total, page=query.page, per_page=query.per_page, items=query.items
    )

  @staticmethod
  async def post( body: user.UserValidate, db: Session = Depends(get_db), token = Depends(get_token) ):
    query_user = UserModel.create(db, last_name=body.last_name, first_name= body.first_name, phone=body.phone, 
                                  description=body.description)
    db.commit()
    return query_user.id

class UsersSelectResource(HTTPEndpoint):
  @staticmethod
  async def get(db: Session = Depends(get_db), token = Depends(get_token)):
    query_users = UserModel.read_select()
    return query_users

class UserResource(HTTPEndpoint):
  @staticmethod
  async def get(user_id: str, db: Session = Depends(get_db), token = Depends(get_token)):
    # query_user = UserModel.read(user_id)
    query_user = UserModel.query.filter_by(id=user_id)\
      .join(MessageModel, isouter=True)\
      .first()
      #.join(CashFlowModel, CashFlowModel.user_id == UserModel.id, isouter=True)
    if not query_user:
      raise CustomException(status_code=404, type='NoData',  detail="No existe Usuario")
    print("query_user: ",query_user)
    # query_message = MessageModel.read_by_user_id(query_user.id)
    # query_transation = CashFlowModel.read_by_user_id(query_user.id)
    # print("query_user: ",query_user)
    # print("query_user: ",query_user.cash_flow)
    # # return user.UserSchema(query_user,
    # #   prueba=1
    # # )

    return query_user
  
  @staticmethod
  async def put(user_id: str, body: user.UserValidate, db: Session = Depends(get_db), token = Depends(get_token)):
    query_user = UserModel.update(db, str(user_id), last_name=body.last_name, first_name= body.first_name, phone=body.phone,
                                    description=body.description)
    db.commit()
    return
  
  @staticmethod
  async def delete(user_id: str, db: Session = Depends(get_db), token = Depends(get_token)):
    query_user = UserModel.delete(db, user_id)
    db.commit()
    return 


class UserDetailsBasicResource(HTTPEndpoint):
  @staticmethod
  async def get(user_id: str, db: Session = Depends(get_db), token = Depends(get_token)):
    query_user = UserModel.read(user_id)
    # query_user = UserModel.query.filter_by(id=user_id).join(CashFlowModel, CashFlowModel.user_id == UserModel.id, isouter=True).first()
    if not query_user:
      raise CustomException(status_code=404, type='NoData',  detail="No existe Usuario")
    limit = 3
    query_message = MessageModel.read_by_user_id(query_user.id, limit=3, orderBy='id')
    query_transation = CashFlowModel.read_by_user_id(query_user.id, limit=3, orderBy='id')

    query_current_balance = CashFlowModel.read_current_balance(query_user.id)
    query_last_recharge =  CashFlowModel.read_last_recharge(query_user.id)

    return user_detail.UserDetailBasicSchema(
      user_id=query_user.id,
      messages = query_message,
      transations = query_transation,
      current_balance = query_current_balance.credit_total,
      last_recharge = query_last_recharge.credit_amount
    )

class UserRestoreResource(HTTPEndpoint):
  @staticmethod
  async def put(user_id: str, db: Session = Depends(get_db), token = Depends(get_token)):
    query_user = UserModel.restore(db, user_id)
    db.commit()
    return 

  