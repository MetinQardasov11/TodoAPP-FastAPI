from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status
from ..models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix='/auth', tags=['auth'])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


templates = Jinja2Templates(directory='TodoApp/templates')
# router.mount('/static', StaticFiles(directory='TodoApp/static'), name='static')


SECRET_KEY = 'f0b3ba46f04cb0ca7be3d56f0a86e0bc978676dc3cdd8e5cb9d1a8c936f6455e'
ALGORITHM = 'HS256'


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
db_dependecy = Annotated[Session, Depends(get_db)]


@router.get('/login-page')
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get('/register-page')
def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')


class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str
    
   
class Token(BaseModel):
    access_token: str
    token_type: str
    

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependecy, user_request: UserRequest):
    create_user_model = Users(
        username = user_request.username,
        email = user_request.email,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        hashed_password = bcrypt_context.hash(user_request.password),
        role = user_request.role,
        is_active = True,
        phone_number = user_request.phone_number
    )
    
    db.add(create_user_model)
    db.commit()
    return f"User Created Successfully"



@router.post('/token', response_model=Token)
async def login_user_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependecy):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'Bearer'}


