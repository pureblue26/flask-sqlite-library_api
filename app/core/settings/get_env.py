"""配置入口：根据 APP_ENV 加载对应 .env 文件，并选择对应环境的配置类。"""

import os
from pathlib import Path

from dotenv import load_dotenv

from app.core.settings.settings import BaseSettings
from app.core.settings.dev import DevSettings
from app.core.settings.prod import ProdSettings
from app.core.settings.test import TestSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

ENVIRONMENTS = {
    "dev": DevSettings,
    "prod": ProdSettings,
    "test": TestSettings,
}


def _load_env_file(app_env: str) -> None:
    """加载对应环境的 .env 文件（.env.dev / .env.prod / .env.test）。

    override=True：强制覆盖已存在的环境变量（切换环境时刷新配置）。
    """
    env_file = BASE_DIR / f".env.{app_env}"
    load_dotenv(env_file, override=True)


def get_settings() -> BaseSettings:
    """根据 APP_ENV：先加载对应 .env，再返回对应配置实例（默认 dev）。"""
    app_env = os.getenv("APP_ENV", "dev")
    _load_env_file(app_env)  # 关键：加载该环境的配置到环境变量
    return ENVIRONMENTS[app_env]()
