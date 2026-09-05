from pydantic import BaseModel


class HeaderMetaData(BaseModel):
    user_agent: str
    device_type: str
    ip_address: str


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    expires_in: int
