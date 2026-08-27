"""借书记录 schemas：返回给客户端的记录格式。"""

from datetime import datetime

from app.schemas.base import schemasModel


class BorrowRecordOut(schemasModel):
    """一条借书记录的响应格式（含书名，方便用户/管理员查看）。"""
    id: int
    book_id: int
    book_title: str
    borrow_date: datetime
    return_date: datetime | None = None
