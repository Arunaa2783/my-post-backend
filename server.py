import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, create_tables
from models import Post  # SQLAlchemy model
from schemas import PostSchema, PostCreate  # Pydantic models

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on server start
create_tables()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET posts - respond with Pydantic model
@app.get("/posts", response_model=List[PostSchema])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

# POST new post - accept Pydantic model, create SQLAlchemy object
@app.post("/posts", response_model=PostSchema)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    post = Post(title=post_data.title, body=post_data.body)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get("/")
def root():
    return {"message": "Backend is running."}

class PostUpdate(BaseModel):
    title: str
    body: str

@app.put("/posts/{post_id}")
def update_post(post_id: int, updated: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = updated.title
    post.body = updated.body
    db.commit()
    db.refresh(post)
    return post