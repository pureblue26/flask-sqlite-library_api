from sqlalchemy import Integer, String

from sqlalchemy.orm import  Mapped, mapped_column
from app.models.base import BaseModel



class User(BaseModel):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    username:Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    password_hash:Mapped[str] = mapped_column(String(255),nullable=False)
    role:Mapped[str] = mapped_column(String(20),default="user",nullable=False)
