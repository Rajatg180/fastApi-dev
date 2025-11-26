from typing import Optional
from sqlmodel import SQLModel, Field


# this is single model representing a todo item in the database -- which is also a table in the database 
# this is bad practice to have models in the same file as database connection
# we should separate them into different files for better organization and maintainability
# class Todo(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str
#     description: Optional[str] = None
#     completed: bool = False


class TodoBase(SQLModel):
    """
    Base fields shared between create, read, and update operations.
    """
    title: str
    description: Optional[str] = None
    completed: bool = False


class Todo(TodoBase, table=True):
    """
    Model representing a todo item in the database.
    this is also a table in the database.
    it only adds the id field to the base model.
    """
    id: Optional[int] = Field(default=None, primary_key=True)


class TodoCreate(TodoBase):
    """
    Model for creating a new todo item.
    Inherits all fields from TodoBase.
    """
    pass

class TodoRead(TodoBase):
    """
    Model for reading a todo item.
    Inherits all fields from TodoBase and adds the id field.
    """
    id: int


class TodoUpdate(SQLModel):
    """
    Model for updating a todo item.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoDelete(SQLModel):
    """
    Model for deleting a todo item.
    Only the id field is required.
    """
    id: int