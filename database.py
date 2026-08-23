import sqlite3
import config
from models import Book, BookStatus


def get_connection()->sqlite3.Connection:
    conn = sqlite3.connect(config.DB_FILE)
    return conn


def init_db()->None:
    try:
        conn = None
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (config.DB_TABLENAME,))
        if cursor.fetchone() is not None:
            conn.close()
            return None
        else:
            query = """
            CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'available')
            """
            cursor.execute(query)
            conn.commit()
            conn.close()
            return None
    except sqlite3.Error as e:
        print("数据库错误: ",e)
    finally:
        if conn: conn.close()


def create_book(title: str, author: str) -> Book:
    try:
        conn = None
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
        "INSERT INTO books (title,author) VALUES(?, ?)",
        (title,author))
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return Book(book_id,title,author)
    except sqlite3.Error as e:
        print("数据库错误: ",e)
    finally:
        if conn: conn.close()


def get_book_by_id(book_id: int) -> Book | None:
    try:
        conn = None
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
        "SELECT * FROM books WHERE id = ? ",
        ( book_id,))
        result = cursor.fetchone()
        if result is not None:
            return Book(result[0],result[1],result[2],BookStatus(result[3]))
        else:
            print("不存在该ID的书籍")
            return None
    except sqlite3.Error as e:
        print("数据库错误: ",e)
    finally:
        if conn: conn.close()

def get_all_books() -> list[Book]:
    try:
        conn = None
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books ")
        result = cursor.fetchall()
        book_list = [] 
        for book in result:
            books = Book(book[0],book[1],book[2],BookStatus(book[3]))
            book_list.append(books)
        return book_list        
    except sqlite3.Error as e:
       print("数据库错误: ",e)
    finally:
        if conn: conn.close()


def update_book_status(book_id: int, new_status: BookStatus) -> None:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET status = ? WHERE id = ?",(new_status.value,book_id,))
        conn.commit()
        return None
    except sqlite3.Error as e:
       print("数据库错误: ",e)
    finally:
        if conn: conn.close()


def delete_book(book_id: int) -> None:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id =  ?",(book_id,))
        conn.commit()
        return None
    except sqlite3.Error as e:
       print("数据库错误: ",e)
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    init_db()
    # book = get_book_by_id(1)
    # update_book_status(1,BookStatus.AVAILABLE)
    # create_book("测试书","张三")
    delete_book(2)
    books = get_all_books()
    print(books)    
    # book = create_book("三国演义","罗贯中")
    # print(book.id,"\n",book.title,"\n",book.author,"\n",book.status)