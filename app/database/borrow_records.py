from app.models.borrow_record import BorrowRecord
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy import select
from datetime import datetime,timezone
from app.database import books
from app.schemas.book import BookStatus  
from app.models.book import Book

async def borrow_book(session:AsyncSession,book_id:int,user_id:int)->BorrowRecord:

    record = BorrowRecord(
        user_id=user_id,
        book_id=book_id,
        borrow_date=datetime.now(timezone.utc),
    )
    session.add(record)
    book = await session.get(Book, book_id)
    if book:
        book.status = BookStatus.BORROWED.value
    await session.commit()   # 统一提交（两个操作要么都成功，要么抛异常回滚）
    return record  



async def return_book(session:AsyncSession, book_id: int) -> BorrowRecord | None:
    """还书：找到未归还的记录，写 return_date。"""
    result = await session.execute(
        select(BorrowRecord)
        .where(BorrowRecord.book_id == book_id, BorrowRecord.return_date.is_(None))
        .order_by(BorrowRecord.borrow_date.desc())
        .limit(1)
    )
    record = result.scalar_one_or_none()
    if record:
        record.return_date = datetime.now(timezone.utc)   # 写归还时间
        await session.commit()
    return record


async def get_records_by_user(session:AsyncSession, user_id: int) -> list[BorrowRecord]:
    """查某用户的所有借书记录（按借出时间倒序）。"""
    result = await session.execute(
        select(BorrowRecord)
        .where(BorrowRecord.user_id == user_id)
        .order_by(BorrowRecord.borrow_date.desc())
    )
    return list(result.scalars().all())

async def get_records_by_title(session:AsyncSession,title:str)->list[BorrowRecord]:
    result = await session.execute(
        select(BorrowRecord)
        .where(BorrowRecord.book.title == title)
        .order_by(BorrowRecord.borrow_date.desc())
    )
    return  list(result.scalars().all())