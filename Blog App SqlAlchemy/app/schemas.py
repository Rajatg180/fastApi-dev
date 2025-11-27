# app/schemas.py

"""
Pydantic models (schemas) for:
- Request bodies (what client sends)
- Response models (what API returns)
"""

from typing import Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    """
    Shared fields between create and read operations.
    """
    title: str
    content: str


class PostCreate(PostBase):
    """
    Schema for creating a post (request body).
    For now, same as PostBase.
    """
    pass


class PostUpdate(BaseModel):
    """
    Schema for updating a post.
    All fields are optional -> for partial updates.
    """
    title: Optional[str] = None
    content: Optional[str] = None


class PostRead(PostBase):
    """
    Schema for reading a post (response model).
    Includes the id field.
    """
    id: int

    class Config:
        # This allows Pydantic to read data from SQLAlchemy models
        # using attributes instead of dict.
        from_attributes = True  # Pydantic v2 style (orm_mode=True in v1)
