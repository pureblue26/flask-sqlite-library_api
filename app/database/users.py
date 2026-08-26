import asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy import select
from app.models import User

async def  create_user(session:AsyncSession,username:str,password_hash:str)->User:
    user = User(username=username,password_hash=password_hash)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_username(session:AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_id(session:AsyncSession, user_id: int) -> User | None:
    
    return await session.get(User, user_id)


async def get_Users(session:AsyncSession)->list[User]|None:
    result = await session.execute(select(User))   
    return list(result.scalars().all()) 



async def Updata_password(session:AsyncSession,user_id:int,password_hash:str)->User:
    user = await get_user_by_id(session,user_id)
    if user:
        user.password_hash = password_hash
        await session.commit()
        await session.refresh(user)
    return user


async def Delete_User(session:AsyncSession,user_id: int)->None:
    user = await get_user_by_id(session,user_id)
    if user:
        await session.delete(user)
        await session.commit()
        await session.refresh(user)

async def Update_user_name(session:AsyncSession,user_id:int,username:str)->User:
    user = await get_user_by_id(session,user_id)
    if user:
        user.username = username
        await session.commit()
        await session.refresh(user)
    return user