from app.core.settings import get_settings
import app.constant as constant
from app.database import books, base
import app.services.books as books
from app.services import auth
from app.schemas.book import (
    BookCreate,
    BookOut,
    BookNotFoundError,
    BookUnavailableError,
    BookNotBorrowedError,
)
from app.schemas.user import (
    UserOut,
    UserCreate,
    UserLogin,
    UserNotFoundError,
    InvalidTokenError,
    DuplicateUsernameError,
    PermissionDeniedError,
)
from fastapi import FastAPI, Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.token import Token
from app.schemas.borrow_record import BorrowRecordOut
from app.security import oauth
from app.models.user import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    await base.init_db()
    yield

app = FastAPI(title="图书管理 API", version="4.0", lifespan=lifespan)

# 业务路由统一挂到 /api 前缀（前端通过 /api 访问，Nginx 反代到后端）
api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发期允许所有来源；生产环境收紧为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- 异常处理 ----
@app.exception_handler(BookNotFoundError)
async def handle_not_found(request, exc):
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(BookUnavailableError)
async def handle_unavailable(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})


@app.exception_handler(BookNotBorrowedError)
async def handle_not_borrowed(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})


@app.exception_handler(InvalidTokenError)
async def handle_invalid_token(request, exc):
    return JSONResponse(status_code=401, content={"message": str(exc)})


@app.exception_handler(UserNotFoundError)
async def handle_user_not_found(request, exc):
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(DuplicateUsernameError)
async def handle_duplicate_username(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})


@app.exception_handler(PermissionDeniedError)
async def handle_permission_denied(request, exc):
    return JSONResponse(status_code=403, content={"message": str(exc)})


# ---- 图书接口 ----
@api_router.get("/books", response_model=list[BookOut])
async def list_books(
    q: str | None = None,
    session: AsyncSession = Depends(base.get_session),
):
    if q:
        return await books.search_books(session, q)
    return await books.get_books(session)


@api_router.post("/books", response_model=BookOut, status_code=201)
async def create_book(
    book_in: BookCreate,
    session: AsyncSession = Depends(base.get_session),
    admin: User = Depends(oauth.get_current_admin),  # 管理员才能建书
):
    return await books.create_book(session, **book_in.model_dump())


@api_router.get("/books/{book_id}", response_model=BookOut)
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(base.get_session),
):
    return await books.get_book(session, book_id)


@api_router.post("/books/{book_id}/borrow", response_model=BookOut)
async def borrow_book(
    book_id: int,
    session: AsyncSession = Depends(base.get_session),
    current_user: User = Depends(oauth.get_current_user),  # 受保护！
):
    return await books.borrow_book(session, book_id, current_user.id)


@api_router.post("/books/{book_id}/return", response_model=BookOut, status_code=200)
async def return_book(
    book_id: int,
    session: AsyncSession = Depends(base.get_session),
    current_user: User = Depends(oauth.get_current_user),  # 受保护！
):
    return await books.return_book(session, book_id)


@api_router.post("/books/{book_id}/delete", status_code=200)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(base.get_session),
    admin: User = Depends(oauth.get_current_admin),  # 管理员才能删书
):
    await books.get_book(session, book_id)
    await books.delete_book(session, book_id)
    return {"message": constant.SUCCESS_DELETE_BOOK}


# ---- 认证接口 ----
@api_router.post("/register", response_model=UserOut, status_code=201)
async def register(
    user_in: UserCreate,
    session: AsyncSession = Depends(base.get_session),
):
    """注册：用户名 + 明文密码。"""
    return await auth.register(session, user_in.username, user_in.password)


@api_router.post("/login", response_model=Token)
async def login(
    user_in: UserLogin,
    session: AsyncSession = Depends(base.get_session),
):
    """登录：验证用户名密码 → 返回 token。"""
    return await auth.user_login(session, user_in.username, user_in.password)


@api_router.get("/users/me", response_model=UserOut)
async def get_me(current_user: User = Depends(oauth.get_current_user)):
    """获取当前登录用户信息（身份来自 token，不传 id）。"""
    return UserOut.model_validate(current_user)


@api_router.post("/users/me/update-name", response_model=UserOut)
async def update_username(
    new_username: str,
    session: AsyncSession = Depends(base.get_session),
    current_user: User = Depends(oauth.get_current_user),
):
    """修改当前用户的名字（身份来自 token）。"""
    return await auth.update_username(session, current_user.id, new_username)


@api_router.post("/users/me/update-password", response_model=UserOut)
async def update_password(
    new_password: str,
    session: AsyncSession = Depends(base.get_session),
    current_user: User = Depends(oauth.get_current_user),
):
    """修改当前用户的密码（身份来自 token）。"""
    return await auth.update_password(session, current_user.id, new_password)


@api_router.delete("/users/me", status_code=200)
async def delete_me(
    session: AsyncSession = Depends(base.get_session),
    current_user: User = Depends(oauth.get_current_user),
):
    """注销当前用户（身份来自 token）。"""
    await auth.delete_user(session, current_user.id)
    return {"message": constant.SUCCESS_DELETE_BOOK}


@api_router.get("/users/me/records", response_model=list[BorrowRecordOut])
async def get_my_records(
    session: AsyncSession = Depends(base.get_session),
    current_user: User = Depends(oauth.get_current_user),
):
    """当前用户的借书记录（只看自己的）。"""
    return await books.get_my_records(session, current_user.id)


@api_router.get("/admin/records", response_model=list[BorrowRecordOut])
async def admin_records_by_title(
    title: str,
    session: AsyncSession = Depends(base.get_session),
    admin: User = Depends(oauth.get_current_admin),
):
    """管理员：按书名查借书记录。"""
    return await books.get_records_by_title(session, title)


@app.get("/")
def root():
    return "欢迎来到图书馆"

# 注册业务路由（/api 前缀）
app.include_router(api_router)


async def main():
    await base.init_db()

if __name__ == "__main__":
    asyncio.run(main())

