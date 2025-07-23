import os
import time
import logging
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rootroot@localhost:5432/postdb"

# Retry until the database is available
MAX_RETRIES = 10
for attempt in range(MAX_RETRIES):
    try:
        logger.info("Trying to connect to PostgreSQL...")
        conn = psycopg2.connect(SQLALCHEMY_DATABASE_URL)
        conn.close()
        logger.info("Database connection established.")
        break
    except psycopg2.OperationalError as e:
        logger.warning(f"Database not ready (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
        time.sleep(2)
else:
    logger.error("Failed to connect to the database after multiple attempts.")
    raise RuntimeError("Database not available")

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

def create_tables():
    Base.metadata.create_all(bind=engine)
