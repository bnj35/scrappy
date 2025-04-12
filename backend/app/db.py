from sqlalchemy import create_engine, Column, Integer, String, Text, Date, TIMESTAMP, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/job_scraper")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    contract = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    date = Column(String(100), nullable=True)
    offer_url = Column(Text, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    status = Column(String(20), default="active")

    __table_args__ = (UniqueConstraint("source", "offer_url", name="unique_source_offer_url"),)