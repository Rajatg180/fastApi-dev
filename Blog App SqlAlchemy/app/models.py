"""
SQLAlchemy ORM models: these describe database tables.
"""
from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Post(Base):
    __tablename__ = "posts" # table name in db

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False,index=True)
    content = Column(Text,nullable=False)