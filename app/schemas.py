from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel, Field


class UserPlain(BaseModel):
    name: str

class UserBase(UserPlain):
    email: str

class UserCreate(UserBase):
    password: str

class BlogBase(BaseModel):
    title: str
    body: str
    thumbnail: bytes | None = None

class BlogCreate(BlogBase):
    pub_datetime: datetime = Field(default_factory=datetime.now)

class User(UserBase):
    hashed_password: str
    is_author: bool
    blogs: list[BlogBase]

    class Config:
        orm_mode = True

# class CommentBase(BaseModel):
#     author: UserPlain
#     comment: str

# class CommentDB(CommentBase):
#     pub_datetime: datetime = Field(default_factory=datetime.now)

class Blog(BlogBase):
    # author: UserBase
    # comments: list[CommentDB]
    
    class Config:
        orm_mode = True
