
from fastapi import FastAPI


app = FastAPI()

@app.get("/execute_sql")
def execute_sql():
    return "learning SQL with FastAPI";