from fastapi import APIRouter
from typing import List, Optional, Union

from app.database.get_db import get_db

from app.middlewares.auth_db import AuthDbMiddleware

from app.schemas import message, message_detail ,pagination

from app.resources.message import MessagesResource, MessageResource, MessageDetailsResource

router = APIRouter(
  prefix='/messages',
  tags=["messages"],
  route_class=AuthDbMiddleware
)

# Messages Pagination and Save
router.add_api_route("",
  MessagesResource.get,
  methods=['GET'],
  name="Show all messages pagination",
  response_model=pagination.PaginationsBase[List[message.MessagePaginationSchema]]
)

# Messages Id
router.add_api_route("/{message_id}", 
  MessageResource.get, 
  methods=['GET'], 
  name="Show one user",
  response_model=message.MessageSchema
)


# Messages Id
router.add_api_route("/{message_id}/details", 
  MessageDetailsResource.get, 
  methods=['GET'], 
  name="Show Message details",
  response_model=List[message_detail.MessageDetailSchema]
)


# router.add_api_route("/{message_id}", 
#   UserResource.put, 
#   methods=['PUT'],
#   name="Modificar one user",
# )


# # User Restore
# router.add_api_route("/{message_id}/restore", 
#   UserRestoreResource.put, 
#   methods=['PUT'],
#   name="Restaurar one user",
# )
