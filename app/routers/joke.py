from fastapi import APIRouter

from app.database.get_db import get_db

from app.middlewares.base_db import BaseDbMiddleware

from app.schemas import joke

from app.resources.joke import RandomJokesResource, JokesResource, JokeResource

router = APIRouter(
  prefix='/jokes',
  tags=["jokes"],
  route_class=BaseDbMiddleware
)

router.add_api_route("/random", 
  RandomJokesResource.get, 
  methods=['GET'],
  name="Mostrar chistes random de servicios",
)

router.add_api_route("", 
  JokesResource.post, 
  methods=['POST'],
  name="Registrar chistes en base de datos",
)

router.add_api_route("/{joke_id}", 
  JokeResource.get, 
  methods=['GET'], 
  name="Mostrar un usuario",
  response_model=joke.JokeBasicSchema
)


router.add_api_route("/{joke_id}", 
  JokeResource.put, 
  methods=['PUT'],
  name="Modificar un chiste que existe",
)

router.add_api_route("/{joke_id}", 
  JokeResource.delete, 
  methods=['DELETE'],
  name="Eliminar un chiste que existe",
)


# # User Select
# router.add_api_route("/list", 
#   UsersSelectResource.get, 
#   methods=['GET'],
#   name="Mostrar usuarios totales sin paginación",
#   response_model=List[Joke.JokeBasicSchema]
# )

# # User Id
# router.add_api_route("/{user_id}", 
#   UserResource.get, 
#   methods=['GET'], 
#   name="Mostrar un usuario",
#   response_model=Joke.UserSchema
# )

# router.add_api_route("/{user_id}", 
#   UserResource.put, 
#   methods=['PUT'],
#   name="Modificar un usuario",
# )

# router.add_api_route("/{Joke_id}", 
#   UserResource.delete, 
#   methods=['DELETE'],
#   name="Desactivar un usuario",
# )
