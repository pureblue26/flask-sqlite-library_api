# 图书管理 API

一个基于 Flask + SQLite 的图书借阅管理后端服务。

## 功能
- 新增图书、查看图书列表/详情
- 借书、还书（带状态校验）
- 删除图书

## 环境配置
- Python 3.10+
- 虚拟环境 venv

## 构建项目
1. 创建虚拟环境并激活：python -m venv .venv
2. 安装依赖：pip install -r requirements.txt
3. 启动服务：python app.py
4. 浏览器打开 http://127.0.0.1:5000

## API 接口
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /books | 获取所有图书 |
| POST | /books | 新增图书 |
| GET | /books/<id> | 获取单本图书 |
| POST | /books/<id>/borrow | 借书 |
| POST | /books/<id>/return | 还书 |
| POST | /books/<id>/delete | 删除图书 |

## 项目结构
config.py   配置信息
models.py   数据模型
database.py 数据存储
services.py 业务逻辑
app.py      路由入口

## 测试
通过 Flask test_client 做了端到端验证