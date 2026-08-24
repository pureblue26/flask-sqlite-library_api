
def test_create_book(client):
    r = client.post("/books", json={"title": "三体", "author": "刘慈欣"})
    assert r.status_code == 201
    assert r.json()["title"] == "三体"


def test_list_books_empty(client):
    r = client.get("/books")
    assert r.status_code == 200
    assert r.json() == []


def test_get_book(client):
    client.post("/books", json={"title": "三体", "author": "刘慈欣"})
    r = client.get("/books/1")
    assert r.status_code == 200
    assert r.json()["title"] == "三体"


def test_get_book_not_found(client):
    r = client.get("/books/99")
    assert r.status_code == 404


def test_borrow_book(client):
    client.post("/books", json={"title": "三体", "author": "刘慈欣"})
    r = client.post("/books/1/borrow")
    assert r.status_code == 200
    assert r.json()["status"] == "borrowed"


def test_borrow_borrowed_book(client):
    client.post("/books", json={"title": "三体", "author": "刘慈欣"})
    client.post("/books/1/borrow")
    r = client.post("/books/1/borrow")
    assert r.status_code == 400


def test_return_book(client):
    client.post("/books", json={"title": "三体", "author": "刘慈欣"})
    client.post("/books/1/borrow")
    r = client.post("/books/1/return")
    assert r.status_code == 200
    assert r.json()["status"] == "available"


def test_return_not_borrowed(client):
    client.post("/books", json={"title": "三体", "author": "刘慈欣"})
    r = client.post("/books/1/return")
    assert r.status_code == 400


def test_search_books(client):
    client.post("/books", json={"title": "三体", "author": "刘慈欣"})
    client.post("/books", json={"title": "三国演义", "author": "罗贯中"})
    r = client.get("/books?q=三")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_delete_book(client):
    client.post("/books", json={"title": "三体", "author": "刘慈欣"})
    r = client.post("/books/1/delete")
    assert r.status_code == 200
    assert client.get("/books/1").status_code == 404
