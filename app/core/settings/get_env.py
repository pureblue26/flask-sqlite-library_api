"""配置入口：根据 APP_ENV 选择对应环境的配置类。"""

import os

from app.core.settings.settings import BaseSettings
from app.core.settings.dev import DevSettings
from app.core.settings.prod import ProdSettings
from app.core.settings.test import TestSettings


ENVIRONMENTS = {
    "dev": DevSettings,
    "prod": ProdSettings,
    "test": TestSettings,
}


def get_settings() -> BaseSettings:
    """根据 APP_ENV 环境变量返回对应配置实例（默认 dev）。"""
    app_env = os.getenv("APP_ENV", "dev")
    return ENVIRONMENTS[app_env]()
