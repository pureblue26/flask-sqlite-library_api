"""4.0 用户管理功能测试（改名/改密码/注销）。"""


def _register_and_login(client, username="张三", password="123456"):
    client.post("/api/register", json={"username": username, "password": password})
    token = client.post("/api/login", json={"username": username, "password": password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_update_username(client):
    """改名字后 /users/me 显示新名字。"""
    headers = _register_and_login(client)
    r = client.post("/api/users/me/update-name", params={"new_username": "李四"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["username"] == "李四"
    # 验证持久化
    r = client.get("/api/users/me", headers=headers)
    assert r.json()["username"] == "李四"


def test_update_password(client):
    """改密码后旧密码登录失败，新密码登录成功。"""
    headers = _register_and_login(client)
    r = client.post("/api/users/me/update-password", params={"new_password": "654321"}, headers=headers)
    assert r.status_code == 200
    # 旧密码登录失败
    assert client.post("/api/login", json={"username": "张三", "password": "123456"}).status_code == 401
    # 新密码登录成功
    assert client.post("/api/login", json={"username": "张三", "password": "654321"}).status_code == 200


def test_delete_me(client):
    """注销后 token 失效（用户不存在 → 401/404）。"""
    headers = _register_and_login(client)
    r = client.delete("/api/users/me", headers=headers)
    assert r.status_code == 200
    # 用旧 token 访问 → 用户已删，应 404（UserNotFoundError）
    r = client.get("/api/users/me", headers=headers)
    assert r.status_code == 404


def test_update_name_requires_auth(client):
    """未登录改名字 → 401。"""
    r = client.post("/api/users/me/update-name", params={"new_username": "李四"})
    assert r.status_code == 401

