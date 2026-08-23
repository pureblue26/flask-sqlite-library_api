
import os
import pytest
import config
import database
from app import app

@pytest.fixture
def client():
    """每个测试前：用临时数据库初始化，返回测试客户端。"""
    config.DB_FILE = config.BASE_DIR / "_test.db"
    if os.path.exists(config.DB_FILE):
        os.remove(config.DB_FILE)      
    database.init_db()                  

    app.config["TESTING"] = True
    yield app.test_client()             

    if os.path.exists(config.DB_FILE):
        os.remove(config.DB_FILE)