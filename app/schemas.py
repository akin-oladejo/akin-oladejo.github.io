from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel, Field, HttpUrl

class Image(BaseModel):
    image_caption: str
    image_url: UploadFile | HttpUrl = 'app\pic3.jpg'
    image_name: str

class User(BaseModel):
    pass

class CommentBase(BaseModel):
    author: User
    comment: str

class CommentIn(CommentBase):
    pub_datetime: datetime = Field(default_factory=datetime.now)

class BlogBase(BaseModel):
    image: Image
    title: str
    author: User
    body: str

class Blog(BlogBase):
    pass

class BlogDB(BlogBase):
    pub_datetime: datetime = Field(default_factory=datetime.now)
