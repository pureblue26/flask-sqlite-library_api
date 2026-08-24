

import asyncio
from app.config import DATABASE_URL
from app.models import Base, Book
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import select
from typing import AsyncGenerator

engine = create_async_engine(DATABASE_URL, echo=False)
SessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)



async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session


async def create_book(session:AsyncSession,title: str, author: str) -> Book:
    book = Book(title=title,author=author)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def get_book_by_id(session:AsyncSession,book_id: int) -> Book | None:
    return await session.get(Book, book_id) 

async def get_all_books(session:AsyncSession) -> list[Book]:
    result = await session.execute(select(Book))   
    return list(result.scalars().all())            


async def update_book_status(session:AsyncSession,book_id: int, new_status: str) -> None:
    book =  await session.get(Book,book_id)
    if book:
        book.status = new_status  
        await session.commit() 



async def delete_book(session:AsyncSession,book_id: int) -> None:
    book =  await session.get(Book,book_id)
    if book:
        await session.delete(book) 
        await session.commit() 


async def search_books(session:AsyncSession,keyword:str)->list[Book]:
    """按书名模糊搜索。无匹配结果时返回空列表。"""
    result = await session.execute(
    select(Book).where(Book.title.like(f"%{keyword}%"))
)
    return list(result.scalars().all())

async def main():
    await init_db()
    async with SessionFactory() as session:
        books = await get_all_books(session)
    for book in books:
        print(book)


if __name__ == "__main__":
    asyncio.run(main())