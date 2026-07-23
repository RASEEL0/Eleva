import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Locally this defaults to the same ./eliva.db 
# In docker-compose, DATABASE_URL points at /app/data/eleva.db, which is
# a mounted volume — so your data survives container restarts/rebuilds.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eliva.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_job = Column(String, nullable=False)
    match_score = Column(Float)
    result_json = Column(Text, nullable=False)  # full pipeline result, stored as JSON text
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)