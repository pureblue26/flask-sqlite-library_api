
from .models import BookBase, BookStatus
import asyncio
import aiosqlite                                    
import app.config as config

async def get_connection()->aiosqlite.Connection:
    return await aiosqlite.connect(config.DB_FILE)


async def init_db()->None:
    try:
        conn = None
        conn = await get_connection()
        cursor = await conn.cursor()
        await cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (config.DB_TABLENAME,))
        if await cursor.fetchone() is not None:
            await conn.close()
            return None
        else:
            query = """
            CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'available')
            """
            await cursor.execute(query)
            await conn.commit()
            return None
    except aiosqlite.Error as e:
        print("数据库错误: ",e)
    finally:
        if  conn: await conn.close()


async def create_book(title: str, author: str) -> BookBase:
    try:
        conn = None
        conn = await get_connection()
        cursor = await conn.cursor()
        await cursor.execute(
        "INSERT INTO books (title,author) VALUES(?, ?)",
        (title,author))
        book_id = cursor.lastrowid
        await conn.commit()
        return BookBase(id=book_id, title=title, author=author)
    except aiosqlite.Error as e:
        print("数据库错误: ",e)
    finally:
        if conn: await conn.close()


async def get_book_by_id(book_id: int) -> BookBase | None:
    try:
        conn = None
        conn = await get_connection()
        cursor = await conn.cursor()
        await cursor.execute(
        "SELECT * FROM books WHERE id = ? ",
        ( book_id,))
        result = await cursor.fetchone()
        if result is not None:
            return BookBase(id=result[0],title = result[1],author=result[2],status=result[3])
        else:
            return None
    except aiosqlite.Error as e:
        print("数据库错误: ",e)
    finally:
        if conn: await conn.close()

async def get_all_books() -> list[BookBase]:
    try:
        conn = None
        conn = await get_connection()
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM books ")
        result = await cursor.fetchall()
        book_list = [] 
        for book in result:
            books = BookBase(id=book[0],title=book[1],author=book[2],status=book[3])
            book_list.append(books)
        return book_list        
    except aiosqlite.Error as e:
       print("数据库错误: ",e)
    finally:
        if conn: await conn.close()


async def update_book_status(book_id: int, new_status: str) -> None:
    try:
        conn = await get_connection()
        cursor = await conn.cursor()
        await cursor.execute("UPDATE books SET status = ? WHERE id = ?",(new_status,book_id,))
        await conn.commit()
        return None
    except aiosqlite.Error as e:
       print("数据库错误: ",e)
    finally:
        if conn: await conn.close()


async def delete_book(book_id: int) -> None:
    try:
        conn = await get_connection()
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM books WHERE id =  ?",(book_id,))
        await conn.commit()
        return None
    except aiosqlite.Error as e:
       print("数据库错误: ",e)
    finally:
        if conn: await conn.close()


async def search_books(keyword:str)->list[BookBase]:
    """按书名模糊搜索。无匹配结果时返回空列表。"""
    try:
        conn = None
        conn = await get_connection()
        cursor = await conn.cursor()
        search_keyword = "%" + keyword +"%"
        await cursor.execute("SELECT * FROM books WHERE title LIKE ?",(search_keyword,))
        result = await cursor.fetchall()
        book_lists = []
        if result:
            for book in result:
                books = BookBase(id=book[0],title=book[1],author=book[2],status=book[3])
                book_lists.append(books)
            return book_lists
        else:
            return book_lists
    except aiosqlite.Error as e:
        print("数据库错误: ",e)
    finally:
        if conn: await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(create_book("活着", "余华"))
