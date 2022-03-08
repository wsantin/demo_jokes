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

class TransationsResource(HTTPEndpoint):
  @staticmethod
  async def get(params: pagination.paginationsValidate = Depends(), 
                db: Session = Depends(get_db), token = Depends(get_token) ):
    print("params: ",params)
    query = CashFlowModel.read_paginate(params)
    print("query: ",query)
    return pagination.PaginationsBase(
      total=query.total, page=query.page, per_page=query.per_page, items=query.items
    )

  @staticmethod
  async def post( body: user.UserValidate, db: Session = Depends(get_db), token = Depends(get_token) ):
    query_user = CashFlowModel.create(db, last_name=body.last_name, first_name= body.first_name, phone=body.phone, 
                                  description=body.description)
    db.commit()
    return query_user.id

class TransationResource(HTTPEndpoint):
  @staticmethod
  async def get(transation_id: str, db: Session = Depends(get_db), token = Depends(get_token)):
    # query_user = CashFlowModel.read(transation_id)
    query_user = CashFlowModel.query.filter_by(id=transation_id).first()
      #.join(CashFlowModel, CashFlowModel.transation_id == CashFlowModel.id, isouter=True)
    if not query_user:
      raise CustomException(status_code=404, type='NoData',  detail="No existe Usuario")
    print("query_user: ",query_user)
    # query_message = MessageModel.read_by_transation_id(query_user.id)
    # query_transation = CashFlowModel.read_by_transation_id(query_user.id)
    # print("query_user: ",query_user)
    # print("query_user: ",query_user.cash_flow)
    # # return user.Transationschema(query_user,
    # #   prueba=1
    # # )
    return query_user
  
  @staticmethod
  async def put(transation_id: str, body: user.UserValidate, db: Session = Depends(get_db), token = Depends(get_token)):
    query_user = CashFlowModel.update(db, str(transation_id), last_name=body.last_name, first_name= body.first_name, phone=body.phone,
                                    description=body.description)
    db.commit()
    return
  
  @staticmethod
  async def delete(transation_id: str, db: Session = Depends(get_db), token = Depends(get_token)):
    query_user = CashFlowModel.delete(db, transation_id)
    db.commit()
    return 


class UserRestoreResource(HTTPEndpoint):
  @staticmethod
  async def put(transation_id: str, db: Session = Depends(get_db), token = Depends(get_token)):
    query_user = CashFlowModel.restore(db, transation_id)
    db.commit()
    return 

  