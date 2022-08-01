# house all utility functions
from passlib.context import CryptContext
from . import database, repo, schemas
import base64
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# load environment variables
load_dotenv()

def get_db():
    """
    Yield the database instance
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Hash:
    """
    Hash and verify passwords
    """

    def __init__(self, plain_pwd=None) -> None:
        # set hash context
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # hash, if plain password provided
        if plain_pwd:
            self.value = self.pwd_context.hash(plain_pwd)

    def verify(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

class UploadFormatException(Exception):
    """
    Just a usual exception. The only special thing is I can pass the name of the file
    """

    def __init__(self, file_name: str, error_message: str) -> None:
        self.file_name = file_name
        self.error_message = error_message

# I never actually used this class below
class CustomUpload:
    """
    A product of overthinking. Say I need to upload a file of a certain type,
    persist it in the SQL db as a base64 encoded string and decode it upon retrieval,
    this class handles just that.
    """

    # def __init__(self, input:UploadFile|None = None) -> None:
    #     if input:
    #         self.input = input
    #         self.is_verified = False
    #         self.is_encoded = False
    #     else: self.input = None

    def verify_input(self, accepted_ext: list = ["image/jpeg", "image/png"]):
        # the default acceptable extensions are jpg and png. Change if you want.
        if self.input:
            if self.input.content_type not in accepted_ext:
                raise UploadFormatException(
                    file_name=self.input.filename,
                    error_message=f"Accepted file types are {accepted_ext}.",
                )
            else:
                self.is_verified = True

    async def encode(self):
        if self.is_verified:
            content = await self.input.read()

            # encode the input into b64 string
            encoded = base64.b64encode(content)
            self.is_encoded = True
            return encoded
        else:
            raise UploadFormatException(
                file_name=self.input.filename,
                error_message="An error occurred verifying the file type.",
            )

    def decode(self):
        if self.is_encoded:
            return self.input.decode("base64")
        else:
            raise UploadFormatException(
                file_name=self.input.filename,
                error_message="This file was not previously encoded.",
            )


# create security dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# convert environment variable SECRET_KEY to string
SECRET_KEY = str(os.environ.get("SECRET_KEY"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         
        sub = payload.get('sub')

        # the value of sub looks like user:<email> or author:<email>...
        # ...so I have to break it into the person type and the email
        
        person_type, email = sub.split(':')
        if email == None:
            raise credentials_exception

        token_data = schemas.TokenData(id=payload.get('id'), email=email, person_type=person_type)
    except JWTError:
        raise credentials_exception
    
    # set is_author to True if decoded token indicates that the person is an author
    is_author = False
    if person_type == 'author': is_author = True 
    person = repo.read_person(db, id=token_data.id, is_author=is_author)
    if not person:
        raise credentials_exception
    return person