"""公共配置：所有环境共有的配置 + 数据库 URL 生成。"""


class BaseSettings:
    """所有环境共有的配置。子类覆盖各自不同的部分。"""

    # 安全
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # 数据库（各环境可覆盖 DB_NAME / DB_HOST 等）
    DB_HOST = "127.0.0.1"
    DB_PORT = 5432
    DB_USER = "library"
    DB_PASSWORD = "library123"
    DB_NAME = "library"

    # 服务
    HOST = "127.0.0.1"
    PORT = 8000
    ORIGIN = "http://localhost:3000"

    @property
    def db_url(self) -> str:
        """生成 SQLAlchemy 异步连接 URL（用当前环境的 DB_* 值）。"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
