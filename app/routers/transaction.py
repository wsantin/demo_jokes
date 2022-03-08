from fastapi import APIRouter
from typing import List, Optional, Union

from app.database.get_db import get_db

from app.middlewares.auth_db import AuthDbMiddleware

from app.schemas import cash_flow, pagination

from app.resources.transation import TransationsResource, TransationResource

router = APIRouter(
  prefix='/transactions',
  tags=["transactions"],
  route_class=AuthDbMiddleware
)

# Messages Pagination and Save
router.add_api_route("",
  TransationsResource.get,
  methods=['GET'],
  name="Show all transactions pagination",
  response_model=pagination.PaginationsBase[List[cash_flow.CashFlowPaginationSchema]]
)

# Messages Id
router.add_api_route("/{message_id}", 
  TransationResource.get, 
  methods=['GET'], 
  name="Show one user",
  response_model=cash_flow.CashFlowSchema
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
