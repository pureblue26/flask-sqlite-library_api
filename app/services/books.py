"""图书业务：查询、创建、删除、借还（借还记录关联用户）。"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.book import (
    BookStatus,
    BookNotFoundError,
    BookUnavailableError,
    BookNotBorrowedError,
    BookOut,
)
from app import constant
from app.database import books as books_db
from app.database import borrow_records as records_db
from app.models.book import Book
from app.schemas.borrow_record import BorrowRecordOut


async def borrow_book(session: AsyncSession, book_id: int, user_id: int) -> BookOut:
    """借书：判断书状态 → 建借书记录 + 改书状态（事务）。"""
    book = await books_db.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(constant.FAIL_BOOK_NOT_FOUND.format(book_id=book_id))
    if book.status == BookStatus.BORROWED.value:
        raise BookUnavailableError(constant.FAIL_BOOK_ALREADY_BORROWED.format(book_id=book_id))

    await records_db.borrow_book(session, book_id, user_id)  # 建记录 + 改状态（事务）
    updated = await books_db.get_book_by_id(session, book_id)
    return BookOut.model_validate(updated)


async def return_book(session: AsyncSession, book_id: int) -> BookOut:
    """还书：判断书状态 → 写归还时间 + 改书状态。"""
    book = await books_db.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(constant.FAIL_BOOK_NOT_FOUND.format(book_id=book_id))
    if book.status == BookStatus.AVAILABLE.value:
        raise BookNotBorrowedError(constant.FAIL_BOOK_NOT_BORROWED.format(book_id=book_id))

    record = await records_db.return_book(session, book_id)  # 写 return_date
    if record:
        await books_db.update_book_status(session, book_id, BookStatus.AVAILABLE.value)
    updated = await books_db.get_book_by_id(session, book_id)
    return BookOut.model_validate(updated)


async def get_book(session: AsyncSession, book_id: int) -> BookOut:
    book = await books_db.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(constant.FAIL_BOOK_NOT_FOUND.format(book_id=book_id))
    return BookOut.model_validate(book)


async def get_books(session: AsyncSession) -> list[BookOut]:
    books = await books_db.get_all_books(session)
    return [BookOut.model_validate(b) for b in books]


async def search_books(session: AsyncSession, keyword: str) -> list[BookOut]:
    books = await books_db.search_books(session, keyword)
    return [BookOut.model_validate(b) for b in books]


async def create_book(session: AsyncSession, title: str, author: str, published_year: int | None = None) -> BookOut:
    return await books_db.create_book(session, title=title, author=author, published_year=published_year)


async def delete_book(session: AsyncSession, book_id: int) -> None:
    return await books_db.delete_book(session, book_id)


def _record_to_out(record) -> BorrowRecordOut:
    """ORM 借书记录 → 响应格式（含书名，通过 relationship 拿 book.title）。"""
    return BorrowRecordOut(
        id=record.id,
        book_id=record.book_id,
        book_title=record.book.title,
        borrow_date=record.borrow_date,
        return_date=record.return_date,
    )


async def get_my_records(session: AsyncSession, user_id: int) -> list[BorrowRecordOut]:
    """当前用户的借书记录。"""
    records = await records_db.get_records_by_user(session, user_id)
    return [_record_to_out(r) for r in records]


async def get_records_by_title(session: AsyncSession, title: str) -> list[BorrowRecordOut]:
    """管理员：按书名查借书记录。"""
    records = await records_db.get_records_by_title(session, title)
    return [_record_to_out(r) for r in records]
