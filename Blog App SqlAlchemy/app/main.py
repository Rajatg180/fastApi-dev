"""
Entry point of the application:
- Creates FastAPI app
- Adds middleware (CORS, logging)
- Defines CRUD routes for posts
"""

import time 
from typing import List, Annotated
from fastapi import Body, FastAPI, Depends, HTTPException, Path, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db


# create all database tables
models.Base.metadata.create_all(bind = engine)

# creating fast api instance
app = FastAPI(title="Blog API with FastAPI and SQLAlchemy")

# ------------ middleware -------

# 1) CORS middleware: allows browser apps from other origins to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify your frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2) logging middleware : to log request duration 
@app.middleware("http")
async def log_request_duration(request: Request,call_next):
    start_time = time.time()
    response = await call_next(request) # call_next passes the request to the actual path operation (your endpoint)
    duration = time.time() - start_time
    response.headers["X-Process-Time"] = str(duration) # # Add custom header to the response
    print(f"Request: {request.method} {request.url} completed in {duration:.4f} seconds")
    return response


# ---------routes------------------
@app.get("/", tags=["root"])
def root():
    """
    Simple root endpoint.
    """
    return {"message": "Welcome to the Blog API. Go to /docs to explore."}


@app.post("/posts/",response_model=schemas.PostRead,status_code=status.HTTP_201_CREATED,tags=["posts"])
def create_post(post : Annotated[schemas.PostCreate,Body()], db: Annotated[Session,Depends(get_db)]):
    """
    Create a new blog post.
    """
    db_post = models.Post(title=post.title,content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=List[schemas.PostRead], tags=["posts"])
def list_posts(db : Session = Depends(get_db)):
    """
    Retrieve all blog posts.
    """
    return db.query(models.Post).all()


@app.get("/posts/{post_id}", response_model=schemas.PostRead, tags=["posts"])
def get_post(post_id: Annotated[int,Path()], db: Session = Depends(get_db)):
    """
    Retrieve a single blog post by ID.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=schemas.PostRead, tags=["posts"])
def update_post(
    post_id: Annotated[int,Path()],
    post_update: Annotated[schemas.PostUpdate,Body()],
    db: Annotated[Session,Depends(get_db)]
):
    """
    Update an existing blog post by ID.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post_update.title is not None:
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    
    db.commit()
    db.refresh(post)
    return post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
def delete_post(post_id: Annotated[int,Path()], db: Annotated[Session,Depends(get_db)]):
    """
    Delete a blog post by ID.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return None  # 204 No Content responses should not return a body

