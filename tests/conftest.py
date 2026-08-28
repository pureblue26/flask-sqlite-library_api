"""pytest 共享配置（4.1：PostgreSQL 版，测试专用 NullPool 引擎）。

关键：测试用独立引擎（NullPool，每次新连接），
避免 TestClient 与全局引擎连接池的事件循环冲突。
"""

import asyncio
import os

# 强制测试使用 test 环境（必须在 import app 之前设置）
os.environ["APP_ENV"] = "test"

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.settings import get_settings
from app.models.base import BaseModel
from app.main import app


@pytest.fixture
def client():
    """每个测试前：建测试引擎、建表、清空，返回 FastAPI TestClient。"""
    engine = create_async_engine(get_settings().db_url, poolclass=NullPool)
    TestSession = async_sessionmaker(engine, expire_on_commit=False)

    async def setup():
        # 建表（幂等，books + users + borrow_records）
        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
        # 清空表（注意顺序：先清被外键引用的表，用 CASCADE 处理关联）
        async with TestSession() as session:
            await session.execute(
                text("TRUNCATE TABLE borrow_records, books, users RESTART IDENTITY CASCADE")
            )
            await session.commit()

    asyncio.run(setup())

    from fastapi.testclient import TestClient

    # 让应用依赖注入使用测试的 Session 工厂（注意：在 database.base）
    from app.database import base as database_base
    original_factory = database_base.SessionFactory
    database_base.SessionFactory = TestSession

    # 把 TestSession 挂到 app.state，供测试辅助使用
    app.state.test_session_factory = TestSession

    try:
        yield TestClient(app)
    finally:
        app.state.test_session_factory = None
        database_base.SessionFactory = original_factory
        asyncio.run(engine.dispose())


def make_admin(client, user_id: int) -> None:
    """测试辅助：把用户提升为管理员（模拟 DBA 手动授权）。

    真实项目里"如何产生第一个管理员"是单独的问题（种子脚本），
    测试里直接改库模拟授权。
    """
    from sqlalchemy import text as sa_text

    factory = app.state.test_session_factory

    async def promote():
        async with factory() as session:
            await session.execute(
                sa_text("UPDATE users SET role = 'admin' WHERE id = :uid"),
                {"uid": user_id},
            )
            await session.commit()

    asyncio.run(promote())


def register_and_login(client, username="张三", password="123456"):
    """测试辅助：注册 + 登录，返回 (headers, user_id)。"""
    r = client.post("/api/register", json={"username": username, "password": password})
    user_id = r.json()["id"]
    token = client.post("/api/login", json={"username": username, "password": password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, user_id

