"""测试环境配置。"""

from app.core.settings.settings import BaseSettings


class TestSettings(BaseSettings):
    DEBUG = False
    DB_NAME = "library_test"
    SECRET_KEY = "test-secret"
