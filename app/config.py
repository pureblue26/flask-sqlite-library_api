"""项目配置：所有可变的设置集中在这里。"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---- 数据库（3.0：PostgreSQL）----
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_USER = "library"
DB_PASSWORD = "library123"
DB_NAME = "library"

# SQLAlchemy 异步连接 URL（asyncpg 驱动）
DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ---- 服务配置 ----
HOST = "127.0.0.1"
PORT = 8000
DEBUG = True
ORIGIN = "http://localhost:3000"
