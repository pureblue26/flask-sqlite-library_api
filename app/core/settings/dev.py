"""开发环境配置。"""

import os

from app.core.settings.settings import BaseSettings


class DevSettings(BaseSettings):
    DEBUG = True
    DB_NAME = "library"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
