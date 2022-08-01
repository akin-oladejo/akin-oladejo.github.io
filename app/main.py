from fastapi import Depends, FastAPI, Request, status, HTTPException
from .routers import auth, blog, user, author
from .utils import UploadFormatException
from fastapi.responses import JSONResponse
from . import models, repo, utils, schemas
from .database import engine


tags_metadata = [
    {
        'name':'base',
        'description':'Base endpoints.'
    },
    {
        'name':'auth',
        'description':'The **login** logic that seperates users and authors is also here.'
    },
    {
        'name':'blog',
        'description':'Endpoints for blogposts.'
    },
    {
        'name':'user',
        'description':'Endpoints for users.'
    },
    {
        'name':'author',
        'description':'Endpoints for authors.'
    }
]

app = FastAPI(
    openapi_tags=tags_metadata,
)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(author.router)
app.include_router(auth.router)



# load up and refresh the database
models.Base.metadata.create_all(bind=engine)

@app.exception_handler(UploadFormatException)
def upload_format_handler(request:Request, exc: UploadFormatException):
    return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        content={'detail':f"There is a problem with '{exc.file_name}'. {str.capitalize(exc.error_message)}"}
    )

@app.get('/', tags=['base'])
def home():
    return {'message':'hello world'}

@app.get('/me', tags=['base'], response_model=schemas.Author)
def read_me(current_user: schemas.Author = Depends(utils.get_current_user)):
    return current_user