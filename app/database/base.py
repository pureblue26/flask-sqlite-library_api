from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.models import Book, User, BaseModel
from app.core.settings import get_settings

settings = get_settings()
DATABASE_URL = settings.db_url


engine = create_async_engine(DATABASE_URL, echo=False)
SessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """表结构由 Alembic 迁移管理（应用启动不再自动建表）。

    首次部署请先运行: uv run alembic upgrade head
    这里只检查表是否存在，缺失时给出明确提示。
    """
    async with engine.connect() as conn:
        exists = await conn.run_sync(
            lambda sync_conn: sync_conn.dialect.has_table(sync_conn, "books")
        )
        if not exists:
            raise RuntimeError(
                "数据库表不存在，请先运行迁移: uv run alembic upgrade head"
            )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session