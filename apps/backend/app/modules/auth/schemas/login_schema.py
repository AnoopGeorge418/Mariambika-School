from pydantic import BaseModel, field_validator


class LoginRequestSchema(BaseModel):
    """Credential required to validate user to login."""

    username: str
    password: str

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v: str) -> str:
        v = v.strip()
        if not v:
            return "Please enter the password!"

        return v


class LoginResponseSchema(BaseModel):
    """Response content and the structure that should be returned for user login."""

    message: str
    roles: list[str]
    permissions: list[str]
