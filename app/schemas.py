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
    thumbnail: bytes | None 

class BlogCreate(BlogBase):
    pub_datetime: datetime = Field(default_factory=datetime.now)

class BlogUpdate(BlogBase):
    latest_update : datetime = Field(default_factory=datetime.now)
    
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
    

class ShowBlog(BlogBase):
    id: int | None
    pub_datetime: datetime | None
    latest_update: datetime | None
    # writer_id: UserBase
    # comments: list[CommentDB]

    class Config:
        orm_mode = True


    


