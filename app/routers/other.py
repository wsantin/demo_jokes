from fastapi import APIRouter

from app.database.get_db import get_db

from app.middlewares.base import BaseMiddleware

from app.schemas import joke

from app.resources.other import McmResource, IncrementResource

router = APIRouter(
  prefix='/others',
  tags=["others"],
  route_class=BaseMiddleware
)

router.add_api_route("/mcm", 
  McmResource.get, 
  methods=['GET'],
  name=": Endpoint al que se le pasará un query param llamado “numbers” con una lista de números enteros. La respuesta de este endpoint debe ser el mínimo común múltiplo de ellos",
)

router.add_api_route("/increment", 
  IncrementResource.get, 
  methods=['GET'],
  name="Endpoint al que se le pasará un query param llamado “number” con un número entero. La respuesta será ese número + 1",
)

