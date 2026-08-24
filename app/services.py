from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import (
    BookStatus,
    BookNotFoundError,
    BookUnavailableError,
    BookNotBorrowedError,
    BookOut,
)
import app.database as database
import asyncio

async def borrow_book(session:AsyncSession,book_id: int) -> BookOut:
    
    book = await database.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(f"id={book_id} 的书不存在")
    if book.status == BookStatus.BORROWED.value:
        raise BookUnavailableError(f"id={book_id} 的书已被借出")
    await database.update_book_status(session, book_id, BookStatus.BORROWED.value)
    updated = await database.get_book_by_id(session, book_id)
    return BookOut(id=updated.id, title=updated.title, author=updated.author, status=updated.status)



async def return_book(session:AsyncSession,book_id: int) -> BookOut:

    book = await database.get_book_by_id(session,book_id)
    if book is None:
        raise BookNotFoundError(f"id={book_id} 的书不存在")
    if book.status == BookStatus.AVAILABLE.value:
        raise BookNotBorrowedError(f"id={book_id} 的书还未借出")
    await database.update_book_status(session, book_id, BookStatus.AVAILABLE.value)
    updated = await database.get_book_by_id(session, book_id)
    return BookOut(id=updated.id, title=updated.title, author=updated.author, status=updated.status)


async def get_book(session:AsyncSession,book_id: int)->BookOut:
    
    book = await database.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(f"id={book_id} 的书不存在")
    return BookOut(id=book.id, title=book.title, author=book.author, status=book.status)




async def get_books(session:AsyncSession)->list[BookOut]:
    books = await database.get_all_books(session)
    return [BookOut(id=b.id, title=b.title, author=b.author, status=b.status) for b in books]

async def search_books(session:AsyncSession,keyword:str)->list[BookOut]:
    books = await database.search_books(session,keyword)
    return [BookOut(id=b.id, title=b.title, author=b.author, status=b.status) for b in books]
    


if __name__ == "__main__":
    books = asyncio.run(get_books()) 
    book =asyncio.run(search_books("三"))
    print(book)