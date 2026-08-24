import app.config as config
import app.database as database
import app.services as services
from app.models import (
    BookNotFoundError, 
    BookUnavailableError,
    BookNotBorrowedError,
    BookOut,
    BookCreate,
)
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI(title="图书管理 API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(BookNotFoundError) 
async def handle_not_found(request,exc):
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(BookUnavailableError)
async def handle_unavailable(request,exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})


@app.exception_handler(BookNotBorrowedError)
async def handle_not_borrowed(request,exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})


@app.get("/books",response_model=list[BookOut])
async def list_books(q:str|None = None):
    if q:
        return await services.search_books(q)
    return await services.get_books()



@app.post("/books",response_model=BookOut,status_code=201)
async def create_book(book_in:BookCreate):
    return await database.create_book(**book_in.model_dump())


@app.get("/books/{book_id}",response_model=BookOut)
async def get_book(book_id: int):
    return await services.get_book(book_id)


@app.post("/books/{book_id}/borrow",response_model=BookOut)
async def borrow_book(book_id: int):
    return await services.borrow_book(book_id)


@app.post("/books/{book_id}/return",response_model=BookOut,status_code=200)
async def return_book(book_id: int):
    return await services.return_book(book_id)


@app.post("/books/{book_id}/delete",status_code=200)
async def delete_book(book_id: int):
    await services.get_book(book_id)
    await database.delete_book(book_id)
    return {"message": "删除成功"}

@app.get("/")
def root():
    return "欢迎来到图书馆"


async def main():
    await database.init_db()

if __name__ == "__main__":
   asyncio.run(main())
