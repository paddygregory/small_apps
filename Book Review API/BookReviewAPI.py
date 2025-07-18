from fastapi import FastAPI, Path
from pydantic import BaseModel
import uvicorn
from typing import Optional
import random

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    rating : float

class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    rating: Optional[float] = None

books = { 
    1: { "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "rating": 4.5 },
    2: { "title": "1984", "author": "George Orwell", "genre": "Dystopian", "rating": 4.0 },
    3: { "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic", "rating": 4.7 },
    4: { "title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Classic", "rating": 4.2 },
    5: { "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "rating": 4.8 },
    6: { "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "rating": 4.9 },
    7: { "title": "The Hunger Games", "author": "Suzanne Collins", "genre": "Dystopian", "rating": 4.3 },
    8: { "title": "The Fault in Our Stars", "author": "John Green", "genre": "Young Adult", "rating": 4.6 },
}

@app.post("/create-book/{book_id}")
def create_book(book_id: int, book: Book):
    if book_id in books:
        return {"Error": "Book ID already exists"}
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

@app.put("/update-book/{book_id}")
def update_book(*, book_id: int, book: UpdateBook):
    if book_id not in books:
        return {"Error": "Book ID does not exist"}
    
    if book.title != None:
        books[book_id]["title"] = book.title
    if book.author != None:
        books[book_id]["author"] = book.author
    if book.genre != None:
        books[book_id]["genre"] = book.genre
    if book.rating != None:
        books[book_id]["rating"] = book.rating
    return books[book_id]

@app.get("/get-book-by-genre-and-rating")
def get_book(genre: str, rating: float):
    matches = []
    for book in books:
        if books[book]["genre"] == genre and books[book]["rating"] >= rating:
            matches.append(books[book])
    return random.choice(matches)