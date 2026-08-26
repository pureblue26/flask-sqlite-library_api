"""用户相关 schemas：注册、返回、登录。"""

from app.schemas.base import schemasModel


class UserCreate(schemasModel):
    """注册请求体：客户端提交明文密码，服务器负责哈希。"""
    username: str
    password: str


class UserOut(schemasModel):
    """返回给客户端的用户信息（绝不含密码！）。"""
    id: int
    username: str


class UserLogin(schemasModel):
    """登录请求体：提交用户名 + 明文密码。"""
    username: str
    password: str


class InvalidTokenError(Exception):
    """令牌无效或过期。"""
    pass


class UserNotFoundError(Exception):
    """用户不存在。"""
    pass


class DuplicateUsernameError(Exception):
    """用户名已存在。"""
    pass