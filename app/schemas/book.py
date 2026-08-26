from enum import Enum
from app.schemas.base import schemasModel 

class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


class BookBase(schemasModel):
   
    id:int | None = None
    title:str
    author:str
    status:str = "available"


class BookCreate(schemasModel):
    title:str
    author:str

class BookOut(BookBase):
    pass

class BookNotFoundError(Exception):
    pass


class BookUnavailableError(Exception):
    pass


class BookNotBorrowedError(Exception):
    pass