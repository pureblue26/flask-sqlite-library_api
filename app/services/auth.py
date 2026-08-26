# app/services/auth.py

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import users as users_db
from app.schemas.user import (
    UserOut,
    InvalidTokenError,
    UserNotFoundError,
    DuplicateUsernameError,
)
from app.security.hash import hash_password, verify_password
from app.security.token import create_access_token
from app.schemas.token import Token
from app.models.user import User




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

async def create_user(session: AsyncSession, username: str, password: str)->UserOut:
    return await register(session,username,password)


async def delete_user(session: AsyncSession, user_id)->str:
    return await users_db.Delete_User(session,user_id)


async def update_user_name(
        session:AsyncSession,
        new_username:str)->UserOut:
    return users_db.Update_user_name(session,new_username)

async def update_user_password(
        session:AsyncSession,
        user_id:int,
        new_password:str)->UserOut:
    hashed = hash_password(new_password)
    return users_db.Updata_password(session,user_id,hashed)

async def get_users(session:AsyncSession)->list[UserOut]:
    return await users_db.get_Users(session)