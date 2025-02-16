from fastapi import FastAPI
from blogs.routers import Blog

app = FastAPI()


app.include_router(Blog.router)