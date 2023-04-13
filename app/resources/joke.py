from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.endpoints import HTTPEndpoint

from app.database.get_db import get_db
from app.utils.jwt import get_token

from app.exceptions.fast_api_custom import CustomException

from app.configs.environment import Config
from app.models.joke import JokesModel
from app.schemas import joke, response
from app.services.chucknorris.chucknorris import ChucknorrisService
from app.services.icanhazdadjoke.icanhazdadjoke import IcanhasdadJokeService

chucknorrisService = ChucknorrisService(Config)
icanhasdadJokeService = IcanhasdadJokeService(Config)

class RandomJokesResource(HTTPEndpoint):
  @staticmethod
  async def get(params: joke.JokeRandomParamValidate = Depends()):
    if params.path == None or params.path == 'Chuck':
      return chucknorrisService.getRandomJokes()
    elif params.path == 'Dad':
      return icanhasdadJokeService.getRandomJokes()
    else:
      raise CustomException(status_code=404, type='NoData',  detail="Validate Path No existe")
  
class JokesResource(HTTPEndpoint):
  @staticmethod
  async def post( body: joke.JokeValidate, db: Session = Depends(get_db) ):
    JokesModel.create(db, description=body.description)
    db.commit()
    return "ok"

class JokeResource(HTTPEndpoint):
  @staticmethod
  async def get(joke_id: str, db: Session = Depends(get_db)):
    query_joke = JokesModel.read(joke_id)
    if not query_joke:
      raise CustomException(status_code=404, type='NoData',  detail="No existe chiste")
    return query_joke

  @staticmethod
  async def put(joke_id: str, body: joke.JokeValidate, db: Session = Depends(get_db)):
    JokesModel.update(db, str(joke_id), description=body.description)
    db.commit()
    return "ok"

  @staticmethod
  async def delete(joke_id: str, db: Session = Depends(get_db)):
    JokesModel.delete(db, joke_id)
    db.commit()
    return "ok"