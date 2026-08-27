import asyncio
from app.database.base import init_db, SessionFactory
from app.database.users import create_user
from app.security.hash import hash_password
import app.config as config

async def seed():
    await init_db()
    async with SessionFactory() as session:
        admin = await create_user(session, config.USER, hash_password(config.USER_PASSWORD))
        admin.role = "admin"      
        await session.commit()
        print(f"管理员创建成功: {admin.username} (id={admin.id})")

if __name__ == "__main__":
    asyncio.run(seed())