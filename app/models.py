from sqlalchemy import Column, Integer, String, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PRAnalysis(Base):
    __tablename__ = "pr_analysis"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True)
    repo_url = Column(String, nullable=False)
    pr_number = Column(Integer, nullable=False)
    results = Column(JSON, nullable=False)

import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("Database URL:", DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

def store_results(repo_url, pr_number, results):
    session = SessionLocal()
    analysis = PRAnalysis(repo_url=repo_url, pr_number=pr_number, results=results)
    session.add(analysis)
    session.commit()
    session.close()

def get_results(repo_url, pr_number):
    session = SessionLocal()
    analysis = session.query(PRAnalysis).filter_by(repo_url=repo_url, pr_number=pr_number).first()
    session.close()
    return analysis.results if analysis else None
