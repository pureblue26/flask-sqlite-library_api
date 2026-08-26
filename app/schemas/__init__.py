"""Pydantic schemas 包：聚合导出，方便 from app.schemas import xxx。"""

from app.schemas.base import schemasModel
from app.schemas.book import (
    BookStatus,
    BookBase,
    BookCreate,
    BookOut,
    BookNotFoundError,
    BookUnavailableError,
    BookNotBorrowedError,
)
from app.schemas.token import Token
from app.schemas.user import (
    UserCreate,
    UserOut,
    UserLogin,
    InvalidTokenError,
    UserNotFoundError,
    DuplicateUsernameError,
)

__all__ = [
    "schemasModel",
    "BookStatus",
    "BookBase",
    "BookCreate",
    "BookOut",
    "BookNotFoundError",
    "BookUnavailableError",
    "BookNotBorrowedError",
    "Token",
    "UserCreate",
    "UserOut",
    "UserLogin",
    "InvalidTokenError",
    "UserNotFoundError",
    "DuplicateUsernameError",
]
