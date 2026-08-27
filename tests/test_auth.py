"""4.0 认证接口测试。"""


def test_register(client):
    """注册成功返回 201，不含密码。"""
    r = client.post("/register", json={"username": "张三", "password": "123456"})
    assert r.status_code == 201
    body = r.json()
    assert body["username"] == "张三"
    assert "password" not in body and "password_hash" not in body


def test_register_duplicate(client):
    """重复用户名注册 → 400。"""
    client.post("/register", json={"username": "张三", "password": "123456"})
    r = client.post("/register", json={"username": "张三", "password": "654321"})
    assert r.status_code == 400


def test_login_success(client):
    """正确密码登录 → 返回 token。"""
    client.post("/register", json={"username": "张三", "password": "123456"})
    r = client.post("/login", json={"username": "张三", "password": "123456"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    """错误密码登录 → 401。"""
    client.post("/register", json={"username": "张三", "password": "123456"})
    r = client.post("/login", json={"username": "张三", "password": "wrong"})
    assert r.status_code == 401


def test_users_me_with_token(client):
    """带 token 访问 /users/me → 返回当前用户。"""
    client.post("/register", json={"username": "张三", "password": "123456"})
    token = client.post("/login", json={"username": "张三", "password": "123456"}).json()["access_token"]
    r = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["username"] == "张三"


def test_users_me_no_token(client):
    """无 token 访问 /users/me → 401。"""
    r = client.get("/users/me")
    assert r.status_code == 401


def test_users_me_fake_token(client):
    """伪 token → 401。"""
    r = client.get("/users/me", headers={"Authorization": "Bearer fake.token.here"})
    assert r.status_code == 401


def test_borrow_requires_auth(client):
    """借书需要登录：无 token → 401。"""
    from tests.conftest import make_admin, register_and_login
    admin_headers, admin_id = register_and_login(client, username="admin")
    make_admin(client, admin_id)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=admin_headers)
    r = client.post("/books/1/borrow")
    assert r.status_code == 401


def test_borrow_with_token(client):
    """带 token 借书 → 成功。"""
    from tests.conftest import make_admin, register_and_login
    admin_headers, admin_id = register_and_login(client, username="admin")
    make_admin(client, admin_id)
    client.post("/books", json={"title": "三体", "author": "刘慈欣"}, headers=admin_headers)
    user_headers, _ = register_and_login(client, username="张三")
    r = client.post("/books/1/borrow", headers=user_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "borrowed"
