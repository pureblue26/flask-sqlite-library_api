from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import (
    BookStatus,
    BookNotFoundError,
    BookUnavailableError,
    BookNotBorrowedError,
    BookOut,
)
from app import constant
import app.database as database
import asyncio

async def borrow_book(session:AsyncSession,book_id: int) -> BookOut:
    
    book = await database.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(constant.FAIL_BOOK_NOT_FOUND.format(book_id=book_id))
    if book.status == BookStatus.BORROWED.value:
        raise BookUnavailableError(constant.FAIL_BOOK_ALREADY_BORROWED.format(book_id=book_id))
    await database.update_book_status(session, book_id, BookStatus.BORROWED.value)
    updated = await database.get_book_by_id(session, book_id)
    return BookOut.model_validate(updated)



async def return_book(session:AsyncSession,book_id: int) -> BookOut:

    book = await database.get_book_by_id(session,book_id)
    if book is None:
        raise BookNotFoundError(constant.FAIL_BOOK_NOT_FOUND.format(book_id=book_id))
    if book.status == BookStatus.AVAILABLE.value:
        raise BookNotBorrowedError(constant.FAIL_BOOK_NOT_BORROWED.format(book_id=book_id))
    await database.update_book_status(session, book_id, BookStatus.AVAILABLE.value)
    updated = await database.get_book_by_id(session, book_id)
    return BookOut.model_validate(updated)


async def get_book(session:AsyncSession,book_id: int)->BookOut:
    
    book = await database.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(constant.FAIL_BOOK_NOT_FOUND.format(book_id=book_id))
    return BookOut.model_validate(book)




async def get_books(session:AsyncSession)->list[BookOut]:
    books = await database.get_all_books(session)
    return [BookOut.model_validate(b) for b in books]

async def search_books(session:AsyncSession,keyword:str)->list[BookOut]:
    books = await database.search_books(session,keyword)
    return [BookOut.model_validate(b) for b in books]
    


if __name__ == "__main__":
    books = asyncio.run(get_books()) 
    book =asyncio.run(search_books("三"))
    print(book)