# Library Management API

A book lending management backend built with **FastAPI + PostgreSQL + SQLAlchemy ORM**, featuring **JWT authentication** (v4.0).

## Features

- 📚 Book management: create, list, get by id, delete
- 🔍 Fuzzy search by title (`?q=keyword`)
- 🔄 Borrow / return books (with status validation, **auth required**)
- 👤 User system: register, login, view profile, update username/password, delete account
- 🔐 JWT authentication (stateless, password hashed with bcrypt)
- ✅ 23 automated tests (pytest)

## Tech Stack

- **Python** 3.12+
- **FastAPI** + Uvicorn (async)
- **PostgreSQL 16** (Docker) + SQLAlchemy ORM (asyncpg)
- **JWT** (python-jose) + **bcrypt** (passlib)
- **uv** package manager
- **pytest** for testing

## Prerequisites

- [uv](https://docs.astral.sh/uv/) package manager
- [Docker](https://www.docker.com/) (for PostgreSQL)

## Quick Start

```bash
# 1. Start PostgreSQL (Docker)
docker compose up -d

# 2. Set up environment variables
cp .env.example .env        # then edit SECRET_KEY etc.

# 3. Install dependencies
uv sync

# 4. Run the server
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

- API root: http://127.0.0.1:8000
- Interactive docs (Swagger UI): http://127.0.0.1:8000/docs

## API Endpoints

### Public

| Method | Path | Description |
|---|---|---|
| POST | /register | Register a new user |
| POST | /login | Login, returns JWT token |

### Books (public read)

| Method | Path | Description |
|---|---|---|
| GET | /books | List all books |
| GET | /books?q=keyword | Fuzzy search by title |
| GET | /books/{id} | Get a book by id |
| POST | /books | Create a book |

### Books (auth required)

| Method | Path | Description |
|---|---|---|
| POST | /books/{id}/borrow | Borrow a book |
| POST | /books/{id}/return | Return a book |
| POST | /books/{id}/delete | Delete a book |

### User (auth required — identity from token, never from client params)

| Method | Path | Description |
|---|---|---|
| GET | /users/me | Get current user profile |
| POST | /users/me/update-name | Update own username |
| POST | /users/me/update-password | Update own password |
| DELETE | /users/me | Delete own account |

## Authentication

All protected endpoints require a JWT token in the request header:

```
Authorization: Bearer <your_token>
```

1. Register: `POST /register` with `{"username": "...", "password": "..."}`
2. Login: `POST /login` → returns `{"access_token": "...", "token_type": "bearer"}`
3. Include the token in subsequent requests.

## Project Structure

```
app/
├── config.py        Configuration (reads from .env)
├── constant.py      Message constants
├── models/          SQLAlchemy ORM models (base/book/user)
├── schemas/         Pydantic models + exceptions (book/user/token)
├── database/        Data access layer (base/books/users)
├── security/        Security (hash/token/oauth)
├── services/        Business logic (books/auth)
└── main.py          FastAPI entry (routing, dependency injection)
```

## Environment Variables

Copy `.env.example` to `.env` and adjust:

| Variable | Description |
|---|---|
| SECRET_KEY | JWT signing key (**use a random secret in production!**) |
| DB_HOST / DB_PORT | PostgreSQL host / port |
| DB_USER / DB_PASSWORD | PostgreSQL credentials |
| DB_NAME | Database name |

Generate a strong secret: `python -c "import secrets; print(secrets.token_hex(32))"`

## Testing

```bash
uv run pytest
```

Uses FastAPI TestClient with a dedicated NullPool test engine (avoids event-loop conflicts) and truncates tables between tests.

## Version History

- v1.0: Flask + sync SQLite (tagged)
- v2.0: FastAPI + async aiosqlite (tagged)
- v3.0: FastAPI + PostgreSQL + SQLAlchemy ORM
- v4.0: JWT authentication + user system (current)
