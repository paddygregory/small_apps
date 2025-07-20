# requirements 

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy import func

# code
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Quote API is running!"}

# database
database = create_engine("sqlite:///quotes.db")

class Quote(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    author: str = Field(index=True, min_length=3, max_length=50)
    quote: str = Field(index=True, min_length=3, max_length=200)

# Create tables AFTER defining the model
SQLModel.metadata.create_all(database)

@app.post("/quotes")
def create_quote(
    quote: Quote = Body(
        ...,
        example={
            "author": "John Doe",
            "quote": "This is a quote"
        },
        description="Quote object to be created"
    )
):
    try:
        with Session(database) as session:
            session.add(quote)
            session.commit()
            session.refresh(quote) 
            print(quote.id)
            return f"Quote {quote.quote} by {quote.author} created successfully"
    except Exception as e:
        return {"error": str(e)}

@app.get("/quotes/{quote_author}")
def get_quotes_by_author(quote_author: str):
    try:
        with Session(database) as session:
            quotes = session.exec(select(Quote).where(Quote.author.like(f"%{quote_author}%"))).all()
            if quotes == None:
                return {"error": f'{quote_author} not found'}
            return quotes
    except Exception as e:
        return {"error": str(e)}

@app.get("/random-quote/{quote_author}")
def get_random_quote(quote_author: str):
    try:
        with Session(database) as session:
            random_quote = session.exec(select(Quote).where(Quote.author.like(f"%{quote_author}%")).order_by(func.random()).limit(1)).first()
            if random_quote == None:
                return {"error": f'{quote_author} not found'}
            return random_quote
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
