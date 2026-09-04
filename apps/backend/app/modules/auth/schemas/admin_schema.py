import uuid

from pydantic import BaseModel

from app.modules.auth.enums.auth_roles_enum import AuthRoles


class AdminCreateSchema(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str
    hashed_password: str
    role: AuthRoles
    is_active: bool
    is_verified: bool
    permissions: list[uuid.UUID] = []
