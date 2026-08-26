from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class Book(BaseModel):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="available", nullable=False)

