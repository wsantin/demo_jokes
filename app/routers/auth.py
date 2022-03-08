from fastapi import APIRouter
from typing import List, Optional, Union

from app.database.get_db import get_db

from app.middlewares.base_db import BaseDbMiddleware

from app.schemas import user, auth, pagination

from app.resources.auth import AuthSignipResource, AuthSignupResource, RecoveryByEmailResource, ActivateUserResource


router = APIRouter(
  prefix='/auth',
  tags=["auth"],
  route_class=BaseDbMiddleware
)

# router.add_api_route("/session",
#   UsersResource.post, 
#   methods=['GET'],
#   name="New Session Login",
# )

router.add_api_route("/signip", 
  AuthSignipResource.post, 
  methods=['POST'],
  name="Register new User",
)

router.add_api_route("/signup", 
  AuthSignupResource.post, 
  methods=['POST'],
  name="Register new User",
)


router.add_api_route("/recovery/email/{email}",
  RecoveryByEmailResource.put, 
  methods=['PUT'], 
  name="Recovery User"
)

router.add_api_route("/recovery/email/{email}/send/otp", 
  RecoveryByEmailResource.put, 
  methods=['PUT'], 
  name="Activate User"
)

router.add_api_route("/active/otp", 
  ActivateUserResource.put, 
  methods=['PUT'], 
  name="Activate User Otp"
)

# router.add_api_route("/active/email/{email}/code/{code_activate}", 
#   ActivateUserResource.put, 
#   methods=['PUT'], 
#   name="Activate User"
# )
