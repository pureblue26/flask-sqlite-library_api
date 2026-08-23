from flask import Flask, jsonify, request
import config
import database
import services
from models import BookNotFoundError, BookUnavailableError, BookNotBorrowedError,Book,BookStatus

app = Flask(__name__)


def books_to_dict(book:Book) -> dict:
    return {"id":book.id,
            "title":book.title,
            "author":book.author,
            "status":book.status.value}

@app.errorhandler(BookNotFoundError)
def handle_not_found(e):
    return {"message": str(e)}, 404


@app.errorhandler(BookUnavailableError)
def handle_unavailable(e):
    return {"message": str(e)}, 400


@app.errorhandler(BookNotBorrowedError)
def handle_not_borrowed(e):
    return {"message": str(e)}, 400


@app.get("/books")
def list_books():
    books = services.get_books()
    return {"books": [books_to_dict(b) for b in books]},200


@app.post("/books")
def create_book():
    data = request.get_json()
    book = database.create_book(data['title'],data['author'])
    return {"book": books_to_dict(book)}, 201


@app.get("/books/<int:book_id>")
def get_book(book_id: int):
    book = services.get_book(book_id)
    return {"book": books_to_dict(book)},200


@app.post("/books/<int:book_id>/borrow")
def borrow_book(book_id: int):
    book = services.borrow_book(book_id)
    return {"book": books_to_dict(book)},200


@app.post("/books/<int:book_id>/return")
def return_book(book_id: int):
    book = services.return_book(book_id)
    return {"book": books_to_dict(book)},200


@app.post("/books/<int:book_id>/delete")
def delete_book(book_id: int):
    services.get_book(book_id)
    database.delete_book(book_id)
    return {"message": "删除成功"}, 200



if __name__ == "__main__":
    database.init_db()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)