# 后端 API 镜像：FastAPI + uv
# PYTHON_IMAGE 可通过 compose 覆盖；默认走国内镜像，避免直连 Docker Hub 失败
ARG PYTHON_IMAGE=docker.m.daocloud.io/library/python:3.12-slim
FROM ${PYTHON_IMAGE}

WORKDIR /app

# 安装 uv（pip 方式，可靠）
RUN pip install --no-cache-dir uv

# 先复制依赖清单并安装（利用 Docker 缓存）
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 复制项目代码
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# 启动：先跑迁移，再启动服务（用 uv run 使用项目虚拟环境）
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
