from dataclasses import dataclass
from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"

@dataclass
class Book:
    id:int
    title:str
    author:str
    status:BookStatus = BookStatus.AVAILABLE


class BookNotFoundError(Exception):
    pass


class BookUnavailableError(Exception):
    pass


class BookNotBorrowedError(Exception):
    pass