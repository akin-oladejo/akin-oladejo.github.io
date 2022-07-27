from fastapi import FastAPI
from .routers import blog, user, author
from .utils import UploadFormatException
from fastapi.responses import JSONResponse
from fastapi import Request, status
from . import models
from .database import engine

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(author.router)


# load up and refresh the database
models.Base.metadata.create_all(bind=engine)

@app.exception_handler(UploadFormatException)
def upload_format_handler(request:Request, exc: UploadFormatException):
    return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        content={'detail':f"There is a problem with '{exc.file_name}'. {str.capitalize(exc.error_message)}"}
    )

@app.get('/')
def home():
    return {'message':'hello world'}