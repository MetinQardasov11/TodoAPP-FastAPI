from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos
from .auth import get_current_user

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
        
db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(max_length=200)
    priority: int = Field(gt=0, lt=6)
    completed: bool

        
        
@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependecy, db: db_dependecy):
    todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
    return todos



@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_one(user: user_dependecy, db: db_dependecy, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    
    raise HTTPException(status_code=404, detail="Todo Not Found")



@router.post('/todo/create', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependecy, db: db_dependecy, todo: TodoRequest):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = Todos(**todo.model_dump(), owner_id = user.get('id'))
    db.add(todo_model)
    db.commit()
    return {"message": "Todo Created Successfully"}



@router.put('/todo/update-todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependecy, todo: TodoRequest, db: db_dependecy, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.completed = todo.completed
    db.commit()
    return {"message": "Todo Updated Successfully"}



@router.delete('/todo/delete-todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependecy, db: db_dependecy, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    
    db.delete(todo_model)
    db.commit()
    return {"message": "Todo Deleted Successfully"}