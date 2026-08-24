"""pytest 共享配置：所有测试文件都能用这里的 fixture（2.0 FastAPI 版）。"""

import os

import pytest

import app.config as config
import app.database as database
from app.main import app


@pytest.fixture
def client():
    """每个测试前：用临时数据库初始化，返回 FastAPI TestClient。"""
    config.DB_FILE = config.BASE_DIR / "_test.db"
    if os.path.exists(config.DB_FILE):
        os.remove(config.DB_FILE)

    # 异步初始化数据库（init_db 是 async 函数）
    import asyncio
    asyncio.run(database.init_db())

    from fastapi.testclient import TestClient
    yield TestClient(app)

    if os.path.exists(config.DB_FILE):
        os.remove(config.DB_FILE)
