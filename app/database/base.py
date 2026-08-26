from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.models import Book, User, BaseModel
from app.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=False)
SessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session