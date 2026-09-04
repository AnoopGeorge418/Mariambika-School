from argon2 import PasswordHasher

hasher = PasswordHasher()


class PasswordUtility:
    """Hashes and verifies password against raw password"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes raw password using argon2."""

        return hasher.hash(password)

    @staticmethod
    def verify_hash(hashed_password: str, password: str) -> bool:
        """Verifies hashed password against raw password and returns True if correct."""

        return hasher.verify(hashed_password, password)
