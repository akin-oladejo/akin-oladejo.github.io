# this file houses all crud logic

from fastapi import HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from . import models, schemas, utils
import base64
from sqlalchemy.exc import IntegrityError

# from fastapi import status, Request
# from fastapi.responses import JSONResponse

get_db = utils.get_db

# -----Blog posts------
def create_post(db: Session, title, body, thumbnail):
    if thumbnail:
        # encode the thumbnail into a b64 string
        thumbnail = base64.b64encode(thumbnail)

    # add `pub_datetime` when values are passed to BlogCreate()
    new_blog = schemas.BlogCreate(title=title, body=body, thumbnail=thumbnail)

    # convert to ORM object
    new_post = models.Blog(**new_blog.dict())

    # save to table
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def read_all_posts(db: Session, skip: int = 0, limit: int = 10):
    posts = db.query(models.Blog).offset(skip).limit(limit).all()

    for post in posts:
        post.thumbnail.decode("utf-8") if post.thumbnail else ...
    return posts


def read_post(db: Session, post_id):
    post = db.query(models.Blog).filter(models.Blog.id == post_id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blogpost is unavailable."
        )
    # decode the string representation of the thumbnail if it exists
    if post.thumbnail:
        post.thumbnail = post.thumbnail.decode("utf-8")
    return post


def update_post(db: Session, post_id: int, title, body, thumbnail):
    # fetch post in db using post_id
    post = db.query(models.Blog).filter(models.Blog.id == post_id)

    # handle unavailable post
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blogpost is unavailable."
        )

    current_values = read_post(db, post_id)

    # if the thumbnail is provided for updating, encode it
    if thumbnail:
        # encode the thumbnail into a b64 string
        thumbnail = base64.b64encode(thumbnail)

    # the SQLAlchemy update function needs a dict
    update_values = schemas.BlogUpdate(
        title=title or current_values.title,
        body=body or current_values.body,
        thumbnail=thumbnail or current_values.thumbnail,
    )

    post.update(update_values.dict())
    db.commit()
    return "updated"


def delete_post(db: Session, post_id: int):
    post = db.query(models.Blog).filter(models.Blog.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blogpost is unavailable."
        )
    post.delete(synchronize_session=False)
    db.commit()
    # delete operation does not return value


# -----Users/Authors------
def create_person(db: Session, person, is_author=False):
    # choose btw author table and user table
    target_table = models.Author if is_author else models.User

    # hash password
    hashed_pwd = utils.Hash(person.password).value

    if is_author:
        # use the Author schema for authors
        parsed = schemas.Author(**person.dict())  # adds a blog attribute
    else:
        # use the User schema for authors
        parsed = schemas.User(**person.dict())

    new_entry = target_table(**parsed.dict(), hashed_password=hashed_pwd)
    
    try:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Email already exists.'
        )
    return new_entry


def read_persons(db: Session, skip: int = 0, limit: int = 100, is_author=False):
    # choose btw author table and user table
    target_table = models.Author if is_author else models.User

    new_query = db.query(target_table).offset(skip).limit(limit).all()

    return new_query


def read_person(db: Session, id: int, is_author=False):
    # choose btw author table and user table
    target_table = models.Author if is_author else models.User
    person_type = "Author" if is_author else "User"

    person = db.query(target_table).filter(id == target_table.id).first()

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{person_type} is unavailable",
        )

    return person


def update_password(password: str):
    ...

def update_person(db: Session, id, name, email, is_author: bool = False):
    # choose btw author table and user table
    target_table = models.Author if is_author else models.User
    person_type = "Author" if is_author else "User"

    # fetch post in db using post_imodels.Blogd
    person = db.query(target_table).filter(target_table.id == id)

    # handle unavailable post
    if not person.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{person_type} is unavailable.",
        )

    current_values = (
        # if the user is an author, pass is_author=True to read_person()
        read_person(db, id, is_author=True)
        if is_author
        else read_person(db, id)
    )

    # note that email has been changed if a different email was provided
    changed_email = False
    if email:
        if email != current_values.email:
            changed_email = True

    # the SQLAlchemy update function needs a dict
    update_values = schemas.PersonBase(
        name = name or current_values.name,
        email = email or current_values.email
    )

    person.update(update_values.dict())

    

    db.commit()
    return changed_email, "updated"


def delete_person(db: Session, id:int, is_author=False):
    # choose btw author table and user table
    target_table = models.Author if is_author else models.User
    person_type = "Author" if is_author else "User"

    person = db.query(target_table).filter(target_table.id == id)

    if not person.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{person_type} is unavailable."
        )
    person.delete(synchronize_session=False)
    db.commit()
    # delete operation does not return value


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
def create_tag():
    ...


def read_tag():
    ...


def read_all_tags():
    ...


def update_tag():
    ...


def delete_tag():
    ...
