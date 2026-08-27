"""借书记录模型：关联用户和书籍。"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.models.base import BaseModel
from app.models.book import Book


class BorrowRecord(BaseModel):
    """一条借书记录：谁、在什么时候、借了哪本书，归还时间可空（null = 没还）。"""

    __tablename__ = "borrow_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    borrow_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    return_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    book: Mapped["Book"] = relationship()
