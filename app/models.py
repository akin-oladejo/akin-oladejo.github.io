from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from .database import Base

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    thumbnail = Column(LargeBinary, index=True)
    title = Column(String, index=True)
    body = Column(String, index=True)
    pub_datetime = Column(DateTime)
    writer_id = Column(Integer, ForeignKey("users.id"))
    
    # comments = relationship(Integer, ForeignKey)
    writer = relationship('User', back_populates='blogs')

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_author = Column(Boolean)

    blogs = relationship('Blog', back_populates='writer')

# class Comments(Base):
#     __tablename__ = 'comments'

#     writer = 
#     blog_post = 
#     pub_datetime = Column(DateTime)

#     blog_post 
