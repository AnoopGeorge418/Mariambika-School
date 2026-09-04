from enum import Enum


class OtpPurpose(str, Enum):
    VERIFICATION = "verification"
    PASSWORD_RESET = "password_reset"
