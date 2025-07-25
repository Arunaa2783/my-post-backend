import os
import time
import logging
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use environment variable for DB URL (safe way)
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set!")
    raise RuntimeError("DATABASE_URL environment variable is required")

logger.info(f"DATABASE_URL found: {SQLALCHEMY_DATABASE_URL}")

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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

def create_tables():
    Base.metadata.create_all(bind=engine)
