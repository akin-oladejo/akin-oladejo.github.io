from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.orm import relationship

from .database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String, index=True)
    pub_datetime = Column(DateTime)
    latest_update = Column(DateTime)
    thumbnail = Column(LargeBinary, index=True)
    writer_id = Column(Integer, ForeignKey("authors.id"))

    # comments = relationship(Integer, ForeignKey)
    writer = relationship("Author", back_populates="blogs")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    person_type = Column(String)
    hashed_password = Column(String)

    blogs = relationship("Blog", back_populates="writer")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    person_type = Column(String)
    hashed_password = Column(String)


# class Comments(Base):
#     __tablename__ = 'comments'

#     writer =
#     blog_post =
#     pub_datetime = Column(DateTime)

#     blog_post
