from fastapi import APIRouter
from typing import List, Optional, Union

from app.database.get_db import get_db

from app.middlewares.auth_db import AuthDbMiddleware

from app.schemas import user, user_detail ,pagination

from app.resources.user import UsersCustomersResource, UsersOperatorsResource,\
    UsersSelectResource, UserDetailsBasicResource, UserResource, UserRestoreResource

router = APIRouter(
  prefix='/users',
  tags=["users"],
  route_class=AuthDbMiddleware
)

# User Pagination and Save
router.add_api_route("/customers",
  UsersCustomersResource.get,
  methods=['GET'],
  name="Show users customers pagination",
  response_model=pagination.PaginationsBase[List[user.UserBasicSchema]]
)

# User Pagination and Save
router.add_api_route("/operators",
  UsersOperatorsResource.get,
  methods=['GET'],
  name="Show users operators pagination",
  response_model=pagination.PaginationsBase[List[user.UserBasicSchema]]
)

router.add_api_route("/customers", 
  UsersCustomersResource.post, 
  methods=['POST'],
  name="Register user custmomer",
)

router.add_api_route("/operators", 
  UsersOperatorsResource.post, 
  methods=['POST'],
  name="Register user operator",
)

# User Id
router.add_api_route("/{user_id}", 
  UserResource.get, 
  methods=['GET'], 
  name="Show one user",
  response_model=user.UserSchema
)

# User Id
router.add_api_route("/{user_id}/details/basic", 
  UserDetailsBasicResource.get, 
  methods=['GET'], 
  name="Show one user",
  # response_model=user_detail.UserDetailBasicSchema
)

# User Select
router.add_api_route("/select/customers", 
  UsersSelectResource.get, 
  methods=['GET'],
  name="Show users totales sin paginación",
  response_model=List[user.UserSchema]
)

router.add_api_route("/select/operators", 
  UsersSelectResource.get, 
  methods=['GET'],
  name="Show users totales sin paginación",
  response_model=List[user.UserSchema]
)


router.add_api_route("/{user_id}", 
  UserResource.put, 
  methods=['PUT'],
  name="Modificar one user",
)

router.add_api_route("/{user_id}", 
  UserResource.delete, 
  methods=['DELETE'],
  name="Desactivar one user",
)

# User Restore
router.add_api_route("/{user_id}/restore", 
  UserRestoreResource.put, 
  methods=['PUT'],
  name="Restaurar one user",
)
