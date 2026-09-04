from enum import Enum


class AuthRoles(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
