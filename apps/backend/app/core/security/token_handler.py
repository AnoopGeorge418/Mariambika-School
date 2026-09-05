import datetime
import hashlib
import hmac
import secrets
import uuid

import jwt
from fastapi import HTTPException, status

from app.core.config.settings import APP_SETTINGS
from app.modules.auth.enums.auth_roles_enum import AuthRoles


class TokenHandlerSecurity:
    def __init__(self) -> None:
        self.secret_key = APP_SETTINGS.REFRESH_TOKEN_SECRET_KEY
        self.jwt_secret_key = APP_SETTINGS.ACCESS_TOKEN_SECRET_KEY
        self.access_token_expires_in = APP_SETTINGS.ACCESS_TOKEN_EXPIRES_IN
        self.jwt_algorithm = APP_SETTINGS.JWT_TOKEN_ALGORITHM

    def create_refresh_token(self) -> str:
        """Creates refresh token and returns it as raw token."""

        return secrets.token_urlsafe(32)

    def hash_refresh_token(self, raw_refresh_token: str) -> str:
        """ "Hashes raw refresh token using HMAC-SHA256."""

        return hmac.new(
            self.secret_key, raw_refresh_token.encode(), hashlib.sha256
        ).hexdigest()

    def verify_hashed_refresh_token(self, raw_token: str, stored_hash: str):
        """Verifies hashed refreshed token against raw token."""

        computed_hash = self.hash_refresh_token(raw_token)
        return hmac.compare_digest(computed_hash, stored_hash)

    def create_access_token(
        self, admin_id: uuid.UUID, roles: AuthRoles
    ) -> tuple[str, int]:
        """Creates a signed JWT access token. Returns (token, expires_in_seconds)."""

        now = datetime.datetime.now(datetime.UTC)
        expires_at = now + datetime.timedelta(seconds=self.access_token_expires_in)

        payload = {
            "sub": admin_id,
            "role": roles.value,
            "iat": now,
            "exp": expires_at,
            "iss": "maiambika-api",
        }
        if payload["role"] != "SUPER_ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Superadmin access required",
            )

        token = jwt.encode(payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)
        return token, self.access_token_expires_in
