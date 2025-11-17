from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# POSTGRES_DATABASE_URL = "postgresql://postgres:11112003Mm@localhost/TodoApplication"
# MYSQL_DATABASE_URL = "mysql+pymysql://root:11112003mm@127.0.0.1:3306/TodoApplicationDB"
SQLITE_DATABASE_URL = 'sqlite:///./todos.db'

engine = create_engine(SQLITE_DATABASE_URL)
# engine = create_engine(MYSQL_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()