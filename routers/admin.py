from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.sql.functions import user
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from .auth import get_current_user

router = APIRouter(prefix='/admin', tags=['admin'])


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
        
db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]


@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependecy, db: db_dependecy):
    
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Todos).all()



@router.delete('/todo/delete-todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependecy, db: db_dependecy, todo_id: int = Path(gt=0)):
    
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    
    db.delete(todo_model)
    db.commit()
    return {"message": "Todo Deleted Successfully"}