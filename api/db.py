from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

DB_URL = '{}://{}:{}@{}:{}/{}'.format("postgresql+psycopg2", "admin", "password", "db", "5432", "bde_db")
engine = create_engine(DB_URL, echo=True)
Session = scoped_session(
            sessionmaker(
                autocommit = False,
                autoflush = False,
                bind = engine))   

Base = declarative_base()

def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()