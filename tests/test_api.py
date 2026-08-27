"""图书 API 测试（4.1：建书/删书需要管理员，借还需要登录）。"""

from tests.conftest import make_admin, register_and_login


def _admin_headers(client):
    """注册管理员并返回请求头（建书/删书需要）。"""
    headers, user_id = register_and_login(client, username="admin")
    make_admin(client, user_id)
    return headers


def test_create_book(client):
    """管理员建书成功。"""
    headers = _admin_headers(client)
    r = client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=headers)
    assert r.status_code == 201
    assert r.json()["title"] == "三体"


def test_create_book_requires_admin(client):
    """普通用户建书 → 403。"""
    headers, _ = register_and_login(client)
    r = client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=headers)
    assert r.status_code == 403


def test_list_books_empty(client):
    r = client.get("/books")
    assert r.status_code == 200
    assert r.json() == []


def test_get_book(client):
    headers = _admin_headers(client)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=headers)
    r = client.get("/books/1")
    assert r.status_code == 200
    assert r.json()["title"] == "三体"


def test_get_book_not_found(client):
    r = client.get("/books/99")
    assert r.status_code == 404


def test_borrow_book(client):
    admin_headers = _admin_headers(client)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=admin_headers)
    user_headers, _ = register_and_login(client, username="用户甲")
    r = client.post("/books/1/borrow", headers=user_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "borrowed"


def test_borrow_borrowed_book(client):
    admin_headers = _admin_headers(client)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=admin_headers)
    user_headers, _ = register_and_login(client, username="用户甲")
    client.post("/books/1/borrow", headers=user_headers)
    r = client.post("/books/1/borrow", headers=user_headers)
    assert r.status_code == 400


def test_return_book(client):
    admin_headers = _admin_headers(client)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=admin_headers)
    user_headers, _ = register_and_login(client, username="用户甲")
    client.post("/books/1/borrow", headers=user_headers)
    r = client.post("/books/1/return", headers=user_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "available"


def test_return_not_borrowed(client):
    admin_headers = _admin_headers(client)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=admin_headers)
    user_headers, _ = register_and_login(client, username="用户甲")
    r = client.post("/books/1/return", headers=user_headers)
    assert r.status_code == 400


def test_search_books(client):
    headers = _admin_headers(client)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=headers)
    client.post("/books", json={"title": "三国演义", "author": "罗贯中"}, headers=headers)
    r = client.get("/books?q=三")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_delete_book(client):
    headers = _admin_headers(client)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=headers)
    r = client.post("/books/1/delete", headers=headers)
    assert r.status_code == 200
    assert client.get("/books/1").status_code == 404


def test_delete_book_requires_admin(client):
    admin_headers = _admin_headers(client)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=admin_headers)
    user_headers, _ = register_and_login(client, username="用户甲")
    r = client.post("/books/1/delete", headers=user_headers)
    assert r.status_code == 403
