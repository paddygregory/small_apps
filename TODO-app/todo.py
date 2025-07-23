from fastapi import FastAPI, Path, Body, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy import func



app = FastAPI()

class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=3, max_length=50)
    description: str = Field(index=True, min_length=3, max_length=200)

class TodoUpdate(SQLModel, table=False):
    title: Optional[str] = Field(default=None, min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, min_length=3, max_length=200)

@app.get("/")
def head():
    return {"Health check": "OK"}

database_url = "sqlite:///todo.db"
engine = create_engine(database_url)
SQLModel.metadata.create_all(engine)

@app.post("/create-todo")
def create_todo(todo: Todo = Body(
    ...,
    example={
        "title": "Buy groceries",
        "description": "Buy groceries from the store"
    },
    description="Todo object to be created"
)):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return f"Todo created successfully with id {todo.id} and title {todo.title}"

@app.get("/get-todo/{todo_title}")
def get_todo(todo_title: str):
    with Session(engine) as session:
        statement = select(Todo).where(Todo.title == todo_title)
        result = session.exec(statement).first()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail='Todo not found')

@app.put("/update-todo/{todo_title}")
def update_todo(todo_title: str, todo: TodoUpdate = Body(
    ...,
    example={
        "title": "buy groceries",
        "description": "Buy groceries from the store",
    },
    description='Todo object to be updated'
)):
    with Session(engine) as session:
        statement = select(Todo).where(Todo.title == todo_title)
        result = session.exec(statement).first()
        if result:
            if todo.title is not None:
                result.title = todo.title
            else:
                result.title = result.title
            if todo.description is not None:
                result.description = todo.description
            else:
                result.description = result.description
            session.commit()
            session.refresh(result)
            return f"Todo updated successfully with id {result.id} and title {result.title}"
        else:
            raise HTTPException(status_code=404, detail='Todo not found')

@app.delete("/delete-todo/{todo_title}")
def delete_todo(todo_title: str):
    with Session(engine) as session:
        statement = select(Todo).where(Todo.title == todo_title)
        result = session.exec(statement).first()
        if result:
            session.delete(result)
            session.commit()
            return f"Todo deleted successfully with id {result.id} and title {result.title}"
        else:
            raise HTTPException(status_code=404, detail='Todo not found')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)