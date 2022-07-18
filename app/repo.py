from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.encoders import jsonable_encoder
from datetime import datetime


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----Blog posts------
def create_post(db: Session, blog: schemas.BlogBase):
    # add pub_datetime when blog is passed to BlogCreate()
    new_blog = schemas.BlogCreate(**blog.dict())

    # convert to ORM object
    new_post = models.Blog(**new_blog.dict())

    # save to table
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def read_post():
    ...


def read_all_posts():
    ...


def update_post():
    ...


def delete_post():
    ...


# -----Authors------
def create_author():
    ...


def read_author():
    ...


def update_author():
    ...


def delete_author():
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
