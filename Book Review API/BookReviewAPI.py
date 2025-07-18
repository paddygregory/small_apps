from fastapi import FastAPI, Path
from pydantic import BaseModel
import uvicorn
from typing import Optional

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    rating : float

books = { 
    1: { "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "rating": 4.5 }
}

@app.post("/create-book")
def create_book(book: Book):
    return book

@app.get("/get-book/{book_id}")
def get_book(book_id: int = Path(..., description="The ID of the book you want to get")):
    return books[book_id]

@app.get("/get-book")
def all_books():
    return books

@app.delete("/delete-book/{book_id}")
def delete_book(book_id: int):
    del books[book_id]
    return {"message": "Book deleted successfully"}