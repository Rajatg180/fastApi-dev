from fastapi import Body, FastAPI, Path
from .database import create_db_and_tables , get_session
from .models import Todo, TodoCreate, TodoRead, TodoUpdate, TodoDelete
from sqlmodel import Session, select
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List , Annotated

app = FastAPI(title="Todo app with sqlmodel")


# ------ create db tabes on startup event ------
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ------------Routes ------------
# tags is used to group the endpoints in the automatic docs
@app.get("/",tags=["Root"])
def read_root():
    return {"message": "Welcome to the Todo app!"}



# ---- create todo ----
@app.post("/todos/",tags=["Todos"],response_model = TodoRead,status_code=status.HTTP_201_CREATED)
def create_todo(session : Annotated[Session , Depends(get_session)] , todo_create : Annotated[TodoCreate,Body()]):

    todo = Todo.from_orm(todo_create) # create a Todo instance from the TodoCreate model
    session.add(todo)
    session.commit()
    session.refresh(todo) # refresh the instance to get the generated id
    return todo


# ---- read all todos ----
@app.get("/todos/",tags=["Todos"],response_model=List[TodoRead],status_code=status.HTTP_200_OK)
def read_all_todos(session : Session =  Depends(get_session)):
    """ Read all todo """
    todos = session.exec(select(Todo)).all()
    return todos



# ---- read single todo ----
@app.get("/todos/{todo_id}",tags=["Todos"],response_model=TodoRead,status_code=status.HTTP_200_OK)
def read_todo(todo_id : Annotated[int,Path()] , session : Session = Depends(get_session)):
    """ Read a single todo by id """
    todo = session.get(Todo , todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with id {todo_id} not found")
    return todo



# ---- update todo ----
@app.patch(path="/todos/{todo_id}",tags=["Todos"],response_model=TodoRead,status_code=status.HTTP_200_OK)
def update_todo(todo_id : Annotated[int,Path()],todo_update : TodoUpdate,session : Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with id {todo_id} not found")

    # Update only the fields that are provided in the request
    todo_data = todo_update.dict(exclude_unset=True)

    for key, value in todo_data.items():
        setattr(todo, key, value)
    
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


# ---- delete todo ----
@app.delete(path="/todos/{todo_id}",tags=["Todos"],status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id : Annotated[int,Path()] , session : Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with id {todo_id} not found")
    session.delete(todo)
    session.commit()
    return