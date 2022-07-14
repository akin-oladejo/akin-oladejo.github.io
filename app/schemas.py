from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel, Field, HttpUrl

class Image(BaseModel):
    image_caption: str
    image_url: UploadFile | HttpUrl = 'https://images.unsplash.com/photo-1512682479844-0fa51f42b4a4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTh8fGJsYWNrfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=600&q=60'
    image_name: str

class User(BaseModel):
    pass

class BlogBase(BaseModel):
    image: Image
    title: str
    author: User
    body: str

class Blog(BlogBase):
    pass

class BlogDB(BlogBase):
    pub_datetime: datetime = Field(default_factory=datetime.now)
