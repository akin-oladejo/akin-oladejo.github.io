from fastapi import APIRouter, UploadFile
from .. import schemas

router = APIRouter(
    tags=['blog'],
    prefix='/blog'
)

@router.post('/')
async def create_blog(blog:schemas.Blog, image_upload:UploadFile|None = None):
    # if image_upload:
    #     image = await image.read()
    #     image_name = image.filename
    #     blog.image.url = image
    return blog