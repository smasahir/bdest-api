from sqlalchemy import create_engine
from api.models.molecule import Base

DB_URL = '{}://{}:{}@{}:{}/{}'.format("postgresql+psycopg2", "admin", "password", "db", "5432", "bde_db")
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
