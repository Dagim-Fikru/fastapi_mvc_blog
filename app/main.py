from fastapi import FastAPI
from app.routes import auth, post

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(post.router, prefix="/posts", tags=["posts"])