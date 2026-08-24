# 图书管理 API

一个基于 FastAPI + PostgreSQL 的图书借阅管理后端服务（3.0 ORM 版）。

## 功能
- 新增图书、查看图书列表/详情
- 借书、还书（带状态校验）
- 删除图书
- 按书名模糊搜索（`?q=关键词`）

## 环境配置
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 包管理器
- Docker（运行 PostgreSQL）

## 构建项目
1. 启动数据库：`docker compose up -d`
2. 安装依赖：`uv sync`
3. 启动服务：`uv run uvicorn app.main:app --host 127.0.0.1 --port 8000`
4. 浏览器打开 http://127.0.0.1:8000
5. 交互式 API 文档：http://127.0.0.1:8000/docs

## API 接口
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /books | 获取所有图书 |
| GET | /books?q=关键词 | 按书名模糊搜索 |
| POST | /books | 新增图书 |
| GET | /books/{id} | 获取单本图书 |
| POST | /books/{id}/borrow | 借书 |
| POST | /books/{id}/return | 还书 |
| POST | /books/{id}/delete | 删除图书 |

## 项目结构
```
app/
├── config.py   配置信息（DATABASE_URL）
├── models.py   SQLAlchemy ORM 模型（books 表）
├── schemas.py  Pydantic 数据模型 + 异常
├── database.py 数据层（异步引擎 + Session + CRUD）
├── services.py 业务逻辑
└── main.py     FastAPI 路由入口（依赖注入）
```

## 测试
```bash
uv run pytest
```
使用 FastAPI TestClient + pytest fixture（测试专用 NullPool 引擎 + 每次清表）。

## 版本历史
- v1.0：Flask + 同步 SQLite（已打 tag 保留）
- v2.0：FastAPI + 异步 aiosqlite
- v3.0：FastAPI + PostgreSQL + SQLAlchemy ORM（当前）
