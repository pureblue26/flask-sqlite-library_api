"""认证依赖：从请求头取 token、解析出当前用户。"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import base
from app.database.users import get_user_by_id
from app.models.user import User
from app.security.token import decode_token
from app.schemas.user import InvalidTokenError, UserNotFoundError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(base.get_session),
) -> User:
    """解析 token → 查用户 → 返回当前用户。"""
    try:
        payload = decode_token(token)
    except JWTError:
        raise InvalidTokenError("无效的令牌")

    user_id = int(payload["sub"])
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise UserNotFoundError("用户不存在")
    return user
