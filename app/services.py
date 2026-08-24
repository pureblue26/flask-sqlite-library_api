
from app.models import (
    BookBase,
    BookStatus,
    BookNotFoundError,
    BookUnavailableError,
    BookNotBorrowedError,
    BookOut,
)
import app.database as database
import asyncio

async def borrow_book(book_id: int) -> BookOut:
    
    books = await database.get_book_by_id(book_id)
    if books is not None:
        if books.status == BookStatus.BORROWED.value:
            raise BookUnavailableError(f"id = {(book_id)}书籍已经借出")
        else:
            await database.update_book_status(book_id,BookStatus.BORROWED.value)
            book = await database.get_book_by_id(book_id)
            return  BookOut(**book.model_dump())
    else:
        raise BookNotFoundError(f"id = {(book_id)}书籍不存在")



async def return_book(book_id: int) -> BookOut:

    books = await database.get_book_by_id(book_id)
    if books is not None:
        if books.status == BookStatus.AVAILABLE.value:
            raise BookNotBorrowedError(f"id = {(book_id)}书籍还未借出")
        else:
            await database.update_book_status(book_id,BookStatus.AVAILABLE.value)
            book = await database.get_book_by_id(book_id)
            return   BookOut(**book.model_dump())
    else:
        raise BookNotFoundError(f"id = {(book_id)}书籍不存在")



async def get_book(book_id: int)->BookOut:
    
    book = await database.get_book_by_id(book_id)
    if book is not None:
        return BookOut(**book.model_dump())
    else:
        raise BookNotFoundError(f"id = {(book_id)}书籍不存在")



async def get_books()->list[BookOut]:
    books = await database.get_all_books()
    return [BookOut(**item.model_dump()) for item in books]

async def search_books(keyword:str)->list[BookOut]:
    books = await database.search_books(keyword)
    return [BookOut(**item.model_dump()) for item in books]


if __name__ == "__main__":
    books = asyncio.run(get_books()) 
    book =asyncio.run(search_books("三"))
    print(book)