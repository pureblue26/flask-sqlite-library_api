from enum import Enum
from pydantic import BaseModel, ConfigDict

class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


class BookBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int | None = None
    title:str
    author:str
    status:str = "available"


class BookCreate(BaseModel):
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