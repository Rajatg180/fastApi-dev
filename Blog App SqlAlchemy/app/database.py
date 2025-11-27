"""
This file sets up:
- SQLAlchemy engine (connection to DB)
- SessionLocal (factory for DB sessions)
- Base (parent class for ORM models)
- get_db() -> FastAPI dependency to inject DB session
"""

# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="Rajat@1803",   # raw password, no encoding needed
    host="localhost",
    port=5432,
    database="blogdb",
)


# Create SQLAlchemy engine 
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative class definitions 
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
