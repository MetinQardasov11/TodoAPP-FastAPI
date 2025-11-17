import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Todos
from routers.todos import get_current_user, get_db
from database import Base
from main import app


POSTGRES_DATABASE_URL = "postgresql://postgres:11112003Mm@localhost/TodoApplication"

engine = create_engine(POSTGRES_DATABASE_URL)

TestSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def test_todo():
    todos = Todos(
        title = "My Test Todo",
        description = "My Test description",
        priority = 3,
        completed = False,
        owner_id = 1
    )
    
    db = TestSessionLocal()
    db.add(todos)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
    

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def override_get_current_user():
    return {'id': 1, 'username': 'metin11', 'user_role': 'developer'}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)

def test_read_all_authenticated():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK