from collections.abc import Generator

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import config


SQLALCHEMY_DATABASE_URL = f'postgresql://{config.database.POSTGRES_USER}:{config.database.POSTGRES_PASSWORD}@{config.database.POSTGRES_HOST}:{config.database.DATABASE_PORT}/{config.database.POSTGRES_DB}'

# Create a synchronous engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()

Base.metadata.create_all(engine)


# Dependency for getting the database session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
