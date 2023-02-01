from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


DATABASE_URL = "mysql+pymysql://root:@localhost:3306/FIVER2"


engine = create_engine(DATABASE_URL, pool_size=50)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
session1 = SessionLocal()
session2 = SessionLocal()
session3 = SessionLocal()
session4 = SessionLocal()
session5 = SessionLocal()
session6 = SessionLocal()
session7 = SessionLocal()
session8 = SessionLocal()
session9 = SessionLocal()
session10 = SessionLocal()
Base = declarative_base()