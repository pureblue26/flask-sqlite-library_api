"""生产环境配置。"""

import os

from app.core.settings.settings import BaseSettings


class ProdSettings(BaseSettings):
    DEBUG = False
    DB_NAME = "library_prod"
    # 生产密钥必须从环境变量读（无默认值，缺失即启动失败，强制安全）
    SECRET_KEY = os.getenv("SECRET_KEY")
