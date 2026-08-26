from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.book import (
    BookStatus,
    BookNotFoundError,
    BookUnavailableError,
    BookNotBorrowedError,
    BookOut,
)
from app import constant
from app.database import books
import asyncio

async def borrow_book(session:AsyncSession,book_id: int) -> BookOut:
    
    book = await books.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(constant.FAIL_BOOK_NOT_FOUND.format(book_id=book_id))
    if book.status == BookStatus.BORROWED.value:
        raise BookUnavailableError(constant.FAIL_BOOK_ALREADY_BORROWED.format(book_id=book_id))
    await books.update_book_status(session, book_id, BookStatus.BORROWED.value)
    updated = await books.get_book_by_id(session, book_id)
    return BookOut.model_validate(updated)



async def return_book(session:AsyncSession,book_id: int) -> BookOut:

    book = await books.get_book_by_id(session,book_id)
    if book is None:
        raise BookNotFoundError(constant.FAIL_BOOK_NOT_FOUND.format(book_id=book_id))
    if book.status == BookStatus.AVAILABLE.value:
        raise BookNotBorrowedError(constant.FAIL_BOOK_NOT_BORROWED.format(book_id=book_id))
    await books.update_book_status(session, book_id, BookStatus.AVAILABLE.value)
    updated = await books.get_book_by_id(session, book_id)
    return BookOut.model_validate(updated)


async def get_book(session:AsyncSession,book_id: int)->BookOut:
    
    book = await books.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(constant.FAIL_BOOK_NOT_FOUND.format(book_id=book_id))
    return BookOut.model_validate(book)


async def get_books(session:AsyncSession)->list[BookOut]:
    book = await books.get_all_books(session)
    return [BookOut.model_validate(b) for b in book]

async def search_books(session:AsyncSession,keyword:str)->list[BookOut]:
    book = await books.search_books(session,keyword)
    return [BookOut.model_validate(b) for b in book]

async def create_book(session:AsyncSession,title:str,author:str)->BookOut:
    return await books.create_book(session,title=title,author=author)

async def delete_book(session:AsyncSession,book_id)->None:
    return await books.delete_book(session, book_id)



if __name__ == "__main__":
    book = asyncio.run(get_books()) 
    book =asyncio.run(search_books("三"))
    print(book)