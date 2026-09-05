from fastapi import APIRouter

from app.modules.auth.routes.login import login_route
from app.modules.auth.routes.refresh import refresh_route

auth_route = APIRouter(prefix="/auth", tags=["Authentication and Authorization"])

# route registering
auth_route.include_router(router=login_route)
auth_route.include_router(router=refresh_route)
