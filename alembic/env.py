from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 使用我们项目的配置（多环境 + 模型元数据）
from app.core.settings import get_settings
from app.models.base import BaseModel
from app.models import Book, User, BorrowRecord  # noqa: F401  确保模型被注册

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# 用项目的数据库 URL 覆盖 alembic.ini 里的连接
config.set_main_option("sqlalchemy.url", get_settings().db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 告诉 Alembic 我们的模型元数据（用于自动生成迁移）
target_metadata = BaseModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (async engine, since we use asyncpg)."""
    # 用异步引擎（项目使用 asyncpg 驱动）
    from sqlalchemy.ext.asyncio import create_async_engine

    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connection) -> None:
        await connection.run_sync(_run_sync_migrations)

    def _run_sync_migrations(connection) -> None:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

    import asyncio

    async def run() -> None:
        async with connectable.connect() as connection:
            await do_run_migrations(connection)
        await connectable.dispose()

    asyncio.run(run())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
