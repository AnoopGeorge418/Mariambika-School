from enum import Enum


class AuthPermissions(str, Enum):
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"


class Resources(str, Enum):
    ADMINS = "admins"
    STUDENTS = "students"
    TEACHERS = "teachers"
    FINANCE = "finance"
    TRANSPORT = "transport"
    SETTINGS = "settings"
