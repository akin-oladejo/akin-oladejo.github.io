from fastapi import FastAPI
from .routers import blog
from .app_exceptions import ImageFormatException
from fastapi.responses import JSONResponse
from fastapi import Request, status
from . import models
from .database import engine

app = FastAPI()

app.include_router(blog.router)

# @app.get('/blogs')
# def home():
#     return {'message':'hello world'}

# load up and refresh the database
models.Base.metadata.create_all(bind=engine)

@app.exception_handler(ImageFormatException)
def image_format_handler(request:Request, exc: ImageFormatException):
    return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        content={'detail':f"'{exc.file_name}' is not a valid (image) format. Current supported image types are PNG and JPG."}
    )