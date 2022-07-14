from fastapi import FastAPI
from .routers import blog

app = FastAPI()

app.include_router(blog.router)

# @app.get('/blogs')
# def home():
#     return {'message':'hello world'}

