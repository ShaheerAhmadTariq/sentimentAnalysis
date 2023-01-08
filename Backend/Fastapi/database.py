from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

<<<<<<< HEAD
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/FIVER"
engine = create_engine(DATABASE_URL,pool_pre_ping=True)
=======
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/FIVER2"
engine = create_engine(DATABASE_URL)
>>>>>>> 17fc458036566f2870bf97eb49ef9a1380f664c4
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
session1 = SessionLocal()
session2 = SessionLocal()
session3 = SessionLocal()
Base = declarative_base()   