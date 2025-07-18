from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "postgresql://logflarex:logflarex@localhost:5432/logflarex"

# Create database engine
engine = create_engine(DATABASE_URL)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)