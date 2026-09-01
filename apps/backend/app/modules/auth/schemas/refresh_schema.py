from pydantic import BaseModel


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    expires_in: int
