from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_host = '127.0.0.1'
db_user = 'root'
db_name = 'test'
db_password = 'root'

DATABASE_URL = 'mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_password, db_host, db_name)

Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
