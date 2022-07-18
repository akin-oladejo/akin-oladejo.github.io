from http.client import HTTPException
from fastapi import APIRouter, Depends, Request, UploadFile, Form, status
from .. import schemas, repo, models
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..app_exceptions import ImageFormatException
import base64


router = APIRouter(tags=["blog"], prefix="/blog")

get_db = repo.get_db


@router.post("/", response_model=schemas.Blog)
async def create_blog(
    *,
    db: Session = Depends(get_db),
    title: str = Form(default='default value to be set to required later'),
    body: str = Form(default='default value to be set to required later'),
    thumbnail: UploadFile | None = None
):
    '''if thumbnail is provided, make sure it is a jpg or png and convert it to bytes'''
    if thumbnail:
        if thumbnail.content_type not in ['image/jpeg', 'image/png']:
            raise ImageFormatException(thumbnail.filename)
        else: 
            thumbnail = await thumbnail.read()
            thumbnail = base64.b64encode(thumbnail).decode()

    # create the schema representation of the blog
    new_blog = schemas.BlogBase(title=title, body=body, thumbnail=thumbnail)
    
    # call the create_post function
    return repo.create_post(db, new_blog)
