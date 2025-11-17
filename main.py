from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .database import engine
from .routers import auth, todos, admin, users
from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory='TodoApp/templates')
app.mount('/static', StaticFiles(directory='TodoApp/static'), name='static')

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/health')
def health_check():
    return {'status': 'healthy'}




app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)