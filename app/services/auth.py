"""认证业务：注册、登录、用户管理。"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import users as users_db
from app.schemas.user import (
    UserOut,
    InvalidTokenError,
    DuplicateUsernameError,
)
from app.security.hash import hash_password, verify_password
from app.security.token import create_access_token
from app.schemas.token import Token


async def register(session: AsyncSession, username: str, password: str) -> UserOut:
    """注册：查重 → 哈希 → 建用户。用户名重复抛异常。"""
    existing = await users_db.get_user_by_username(session, username)
    if existing:
        raise DuplicateUsernameError("用户名已存在")
    hashed = hash_password(password)
    user = await users_db.create_user(session, username, hashed)
    return UserOut.model_validate(user)


async def user_login(session: AsyncSession, username: str, password: str) -> Token:
    """登录：验证用户名密码 → 签发 token。失败抛异常。"""
    user = await users_db.get_user_by_username(session, username)
    if not user or not verify_password(password, user.password_hash):
        raise InvalidTokenError("用户名或密码错误")
    return Token(access_token=create_access_token(user.id))


async def update_username(
    session: AsyncSession, user_id: int, new_username: str
) -> UserOut:
    """修改用户名。"""
    user = await users_db.update_username(session, user_id, new_username)
    if user is None:
        raise InvalidTokenError("用户不存在")
    return UserOut.model_validate(user)


async def update_password(
    session: AsyncSession, user_id: int, new_password: str
) -> UserOut:
    """修改密码：哈希后更新。"""
    hashed = hash_password(new_password)
    user = await users_db.update_password(session, user_id, hashed)
    if user is None:
        raise InvalidTokenError("用户不存在")
    return UserOut.model_validate(user)


async def delete_user(session: AsyncSession, user_id: int) -> None:
    """删除用户。"""
    await users_db.delete_user(session, user_id)


async def get_users(session: AsyncSession) -> list[UserOut]:
    """列出所有用户。"""
    users = await users_db.get_users(session)
    return [UserOut.model_validate(u) for u in users]
