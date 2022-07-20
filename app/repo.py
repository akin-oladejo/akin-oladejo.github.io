from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from.app_exceptions import UploadFormatException
import base64

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# class CustomUpload:
#     '''
#     A product of overthinking. Say I need to upload a file of a certain type,
#     persist it in the SQL db as a base64 encoded string and decode it upon retrieval,
#     this class handles just that.
#     '''

#     def __init__(self, input:UploadFile|None = None) -> None:
#         if input:
#             self.input = input
#             self.is_verified = False
#             self.is_encoded = False
#         else: self.input = None

#     def verify_input(self, accepted_ext:list = ['image/jpeg', 'image/png']):
#         # the default acceptable extensions are jpg and png. Change if you want.
#         if self.input:
#             if self.input.content_type not in accepted_ext:
#                 raise UploadFormatException(file_name = self.input.filename,
#                                             error_message= f'Accepted file types are {accepted_ext}.')
#             else:
#                 self.is_verified = True

#     async def encode(self):
#         if self.is_verified:
#             content = await self.input.read()

#             # encode the input into b64 string
#             encoded =  base64.b64encode(content)
#             self.is_encoded = True
#             return encoded
#         else:
#             raise UploadFormatException(
#                 file_name=self.input.filename,
#                 error_message='An error occurred verifying the file type.'
#             )

#     def decode(self):
#         if self.is_encoded:
#             return self.input.decode('base64')
#         else:
#             raise UploadFormatException(
#                 file_name=self.input.filename,
#                 error_message='This file was not previously encoded.'
#             )



# -----Blog posts------
def create_post(db: Session, title, body, thumbnail):
    # create the schema representation of the blog
    new_blog = schemas.BlogBase(title=title, body=body, thumbnail=thumbnail)

    # add pub_datetime when blog is passed to BlogCreate()
    new_blog = schemas.BlogCreate(**new_blog.dict())

    # convert to ORM object
    new_post = models.Blog(**new_blog.dict())

    # save to table
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def read_post():
    ...


def read_all_posts(db:Session, skip:int = 0, limit:int = 10):
    posts = db.query(models.Blog).offset(skip).limit(limit).all()
    return posts


def update_post(db:Session):
    ...


def delete_post(db:Session):
    ...


# -----Authors------
def create_author(db:Session):
    ...


def read_author(db:Session):
    ...


def update_author(db:Session):
    ...


def delete_author(db:Session):
    ...


# -----Comments-----
def create_comment():
    ...


def read_comment():
    ...


def read_all_comments():
    ...


def update_comment():
    ...


def delete_comment():
    ...


# -----Tags-----
def create_comment():
    ...


def create_comment():
    ...


def read_comment():
    ...


def read_all_comments():
    ...


def update_comment():
    ...


def delete_comment():
    ...
