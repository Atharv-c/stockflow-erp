from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(
    subject: str,
    expires_minutes: int | None = None,
) -> str:
    """
    Generate a JWT access token.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes
        or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )