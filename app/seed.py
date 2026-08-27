import asyncio
import os

from dotenv import load_dotenv

from app.database.base import init_db, SessionFactory
from app.database.users import create_user
from app.security.hash import hash_password

load_dotenv()

async def seed():
    await init_db()
    admin_username = os.getenv("SEED_USERNAME", "admin")
    admin_password = os.getenv("SEED_PASSWORD", "admin123")
    async with SessionFactory() as session:
        admin = await create_user(session, admin_username, hash_password(admin_password))
        admin.role = "admin"      
        await session.commit()
        print(f"管理员创建成功: {admin.username} (id={admin.id})")

if __name__ == "__main__":
    asyncio.run(seed())