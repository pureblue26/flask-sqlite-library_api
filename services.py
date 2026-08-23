
from models import (
    Book,
    BookStatus,
    BookNotFoundError,
    BookUnavailableError,
    BookNotBorrowedError,
)
import database

def borrow_book(book_id: int) -> Book:
    
    books = database.get_book_by_id(book_id)
    if books is not None:
        if books.status == BookStatus.BORROWED:
            raise BookUnavailableError(f"id = {(book_id)}书籍已经借出")
        else:
            database.update_book_status(book_id,BookStatus.BORROWED)
            return  database.get_book_by_id(book_id)
    else:
        raise BookNotFoundError(f"id = {(book_id)}书籍不存在")



def return_book(book_id: int) -> Book:

    books = database.get_book_by_id(book_id)
    if books is not None:
        if books.status == BookStatus.AVAILABLE:
            raise BookNotBorrowedError(f"id = {(book_id)}书籍还未借出")
        else:
            database.update_book_status(book_id,BookStatus.AVAILABLE)
            return  database.get_book_by_id(book_id)
    else:
        raise BookNotFoundError(f"id = {(book_id)}书籍不存在")



def get_book(book_id: int)->Book:
    
    book = database.get_book_by_id(book_id)
    if book is not None:
        return book
    else:
        raise BookNotFoundError(f"id = {(book_id)}书籍不存在")



def get_books()->list[Book]:
    return database.get_all_books()

def search_books(keyword:str)->list[Book]:
    return database.search_books(keyword)


if __name__ == "__main__":
    books = get_books()