from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, Field, validator
import string


class PersonPlain(BaseModel):
    name: str

class PersonBase(PersonPlain):
    email: EmailStr

    class Config:
        orm_mode = True

class PersonCreate(PersonBase):
    password: str
    # password: str = Field(min_length=8) # make password at least 8 chars

    # # make sure password contains a number and a special character
    # @validator('password')
    # def validate_password(cls, value):
    #     contains_special = False # flag special symbol is present
    #     contains_number = False # flag that number is present
        
    #     for i in value:
    #         if i in list(string.punctuation): contains_special = True
    #         if i in ['0','1','2','3','4','5','6','7','8','9']: contains_number = True
    #     print(f'{contains_number=}\n{contains_special=}')
    #     if contains_special and contains_number:
    #         return value
    #     raise ValueError('Password needs to contain at least one special character and number')

class BlogBase(BaseModel):
    title: str 
    body: str 
    thumbnail: bytes | None
    
    class Config:
        orm_mode = True 

class BlogCreate(BlogBase):
    pub_datetime: datetime = Field(default_factory = datetime.now)

class BlogUpdate(BlogBase):
    latest_update : datetime = Field(default_factory = datetime.now)
    
class Author(PersonBase):
    person_type: str = 'author'
    blogs: list[BlogBase] = []

    class Config:
        orm_mode = True

class AuthorWithID(Author):
    id: int

    class Config:
        orm_mode = True
        
class User(PersonBase):
    person_type: str = 'user'

    class Config:
        orm_mode = True

class ShowBlog(BlogBase):
    id: int | None
    pub_datetime: datetime | None
    latest_update: datetime | None
    writer: PersonBase
    # comments: list[CommentDB]

    class Config:
        orm_mode = True

# class CommentBase(BaseModel):
#     author: PersonPlain
#     comment: str

# class CommentDB(CommentBase):
#     pub_datetime: datetime = Field(default_factory=datetime.now)    
    
class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id: int
    email: EmailStr
    person_type: str
