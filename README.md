# 图书管理 API

一个基于 FastAPI + SQLite 的图书借阅管理后端服务（2.0 异步版）。

## 功能
- 新增图书、查看图书列表/详情
- 借书、还书（带状态校验）
- 删除图书
- 按书名模糊搜索（`?q=关键词`）

## 环境配置
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 包管理器

## 构建项目
1. 安装依赖：`uv sync`
2. 启动服务：`uv run uvicorn app.main:app --host 127.0.0.1 --port 8000`
3. 浏览器打开 http://127.0.0.1:8000
4. 交互式 API 文档：http://127.0.0.1:8000/docs

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
├── config.py   配置信息
├── models.py   Pydantic 数据模型
├── database.py 数据存储（aiosqlite 异步）
├── services.py 业务逻辑
└── main.py     FastAPI 路由入口
```

## 测试
```bash
uv run pytest
```
使用 FastAPI TestClient + pytest fixture（临时数据库隔离）。

## 版本历史
- v1.0：Flask + 同步 SQLite（已打 tag 保留）
- v2.0：FastAPI + 异步 aiosqlite（当前）
- 包管理：uv（pyproject.toml + uv.lock）
