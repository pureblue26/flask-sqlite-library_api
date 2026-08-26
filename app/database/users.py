"""用户数据访问：CRUD。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def create_user(session: AsyncSession, username: str, password_hash: str) -> User:
    user = User(username=username, password_hash=password_hash)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars().all())


async def update_password(session: AsyncSession, user_id: int, password_hash: str) -> User | None:
    user = await get_user_by_id(session, user_id)
    if user:
        user.password_hash = password_hash
        await session.commit()
        await session.refresh(user)
    return user


async def update_username(session: AsyncSession, user_id: int, username: str) -> User | None:
    user = await get_user_by_id(session, user_id)
    if user:
        user.username = username
        await session.commit()
        await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user = await get_user_by_id(session, user_id)
    if user:
        await session.delete(user)
        await session.commit()
