from fastapi import APIRouter, Depends, Request, UploadFile, Form, status
from .. import schemas, repo, models
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
import base64
from ..app_exceptions import UploadFormatException

router = APIRouter(tags=["blog"], prefix="/blog")

get_db = repo.get_db

@router.post("/", response_model=schemas.Blog)
async def create_post(
    *,
    db: Session = Depends(get_db),
    title: str = Form(default='default value to be set to required later'),
    body: str = Form(default='default value to be set to required later'),
    thumbnail:  UploadFile | None = None,
):
    if thumbnail:
        if thumbnail.content_type not in ['image/jpeg', 'image/png']:
            raise UploadFormatException(
                file_name=thumbnail.filename,
                error_message='The current accepted file types are PNG and JPEG'
            )
        else: 
            content = await thumbnail.read()

            # encode the thumbnail into b64 string
            thumbnail =  base64.b64encode(content)
    
    # call the create_post function
    return repo.create_post(db, title, body, thumbnail)

@router.get('/', summary='Get All Blog Posts')
def read_all_posts(db:Session = Depends(get_db), skip:int = 0, limit:int = 10):
    return repo.read_all_posts(db, skip, limit)

@router.get("/{id}")
def read_post(*, db:Session = Depends(get_db), blog_id:int):
    return repo.read_post(db, blog_id=blog_id)
    # remember to decode the string representation of the thumbnail