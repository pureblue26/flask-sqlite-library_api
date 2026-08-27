"""JWT 令牌：签发与验证。"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.settings import get_settings

settings = get_settings()
ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(user_id: int) -> str:
    """签发 JWT：把 user_id 和过期时间放进 payload，用密钥签名。"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """验证 JWT：验签 + 检查过期，返回 payload。"""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
