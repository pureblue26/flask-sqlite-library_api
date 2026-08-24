"""pytest 共享配置（3.0：PostgreSQL 版，测试专用 NullPool 引擎）。

关键：测试用独立引擎（NullPool，每次新连接），
避免 TestClient 与全局引擎连接池的事件循环冲突。
"""

import asyncio

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import DATABASE_URL
from app.models import Base
from app.main import app


@pytest.fixture
def client():
    """每个测试前：建测试引擎、建表、清空，返回 FastAPI TestClient。"""
    # 测试专用引擎：NullPool = 不复用连接（避免事件循环冲突）
    engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
    TestSession = async_sessionmaker(engine, expire_on_commit=False)

    async def setup():
        # 建表（幂等）
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        # 清空表
        async with TestSession() as session:
            await session.execute(text("TRUNCATE TABLE books RESTART IDENTITY"))
            await session.commit()

    asyncio.run(setup())

    from fastapi.testclient import TestClient

    # 让应用依赖注入使用测试的 Session 工厂
    from app import database
    original_factory = database.SessionFactory
    database.SessionFactory = TestSession

    try:
        yield TestClient(app)
    finally:
        database.SessionFactory = original_factory
        asyncio.run(engine.dispose())
