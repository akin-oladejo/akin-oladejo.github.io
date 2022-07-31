import email
from fastapi import Depends, FastAPI, Request, status, HTTPException
from .routers import blog, user, author
from .utils import UploadFormatException, get_db
from fastapi.responses import JSONResponse
from . import models, repo, utils, schemas
from .database import engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt


tags_metadata = [
    {
        'name':'base',
        'description':'Base endpoints. The **login** logic that seperates users and authors is also here.'
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

@app.post('/login', tags=['base'])
def login(db:Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), is_author:bool = False):
    person = repo.resolve_login(db, form_data.username, form_data.password, is_author)
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # prefix the value of the 'sub' key with 'author:' if the is_author argument is True
    # ...else, prefix it with 'user:'
    if is_author:
        access_token = utils.create_access_token(
            data={'sub':f'author:{person.email}', 'id':person.id}
        )
    else:
        access_token = utils.create_access_token(
            data={'sub':f'user:{person.email}', 'id':person.id}
        )
    return {'access_token':access_token, 'token_type':'bearer'}

def get_current_user(db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
         
        sub = payload.get('sub')
        if email == None:
            raise credentials_exception

        # the value of sub looks like user:<email> or author:<email>...
        # ...so I have to break it into the person type and the email
        person_type, email = sub.split(':')
        token_data = schemas.TokenData(id=payload.get('id'), email=email, person_type=person_type)
    except JWTError:
        raise credentials_exception
    
    # set is_author to True if decoded token indicates that the person is an author
    if person_type == 'author': is_author = True 
    user = repo.read_person(db, id=token_data.id, is_author=is_author)
    if not user:
        raise credentials_exception
    return user