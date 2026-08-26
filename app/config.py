"""项目配置：所有可变的设置集中在这里。"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# 加载 .env 文件（本地密钥等；部署时用系统环境变量覆盖）
load_dotenv(BASE_DIR / ".env")

# ---- 安全（从环境变量读取，绝不硬编码进代码）----
# 开发时从 .env 文件读；部署时从系统环境变量读
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ---- 数据库（3.0：PostgreSQL）----
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "library")
DB_PASSWORD = os.getenv("DB_PASSWORD", "library123")
DB_NAME = os.getenv("DB_NAME", "library")

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
