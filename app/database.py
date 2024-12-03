from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for defining models
Base = declarative_base()

def get_db():
    """
    Dependency for obtaining a database session in FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
