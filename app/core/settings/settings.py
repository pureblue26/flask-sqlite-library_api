"""公共配置：所有环境共有的配置，实例化时从环境变量读取。"""

import os


class BaseSettings:
    """所有环境共有的配置。子类覆盖各自不同的部分。

    注意：配置在 __init__（实例化）时读取环境变量 —— 因为 .env 文件
    在 get_settings() 中加载，类定义时（import 阶段）还没加载完成。
    """

    def __init__(self):
        # 安全
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.SECRET_KEY = os.getenv("SECRET_KEY")  # 无默认值

        # 数据库（无默认值，必须从 .env.* 提供）
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = int(os.getenv("DB_PORT", "5432"))
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")

        # 服务
        self.HOST = os.getenv("HOST", "127.0.0.1")
        self.PORT = int(os.getenv("PORT", "8000"))
        self.ORIGIN = os.getenv("ORIGIN", "http://localhost:3000")

        # 环境特有
        self.DEBUG = False  # 子类覆盖

    @property
    def db_url(self) -> str:
        """生成 SQLAlchemy 异步连接 URL（用当前环境的 DB_* 值）。"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
