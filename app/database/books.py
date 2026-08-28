
import asyncio
from app.models import Book
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy import select


async def create_book(session:AsyncSession,title: str, author: str, published_year: int | None = None) -> Book:
    book = Book(title=title,author=author,published_year=published_year)
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
    pass


if __name__ == "__main__":
    asyncio.run(main())