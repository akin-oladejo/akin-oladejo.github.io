from fastapi import APIRouter, Depends, UploadFile, Form, status, HTTPException
from .. import schemas, repo, utils
from sqlalchemy.orm import Session
from ..utils import UploadFormatException

router = APIRouter(tags=["blog"], prefix="/blog")

get_db = utils.get_db

# create a single post
@router.post("/", response_model=schemas.ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_post(
    *,
    db: Session = Depends(get_db),
    title: str = Form(default="default value to be set to required later"),
    body: str = Form(default="default value to be set to required later"),
    thumbnail: UploadFile | None = None,
    creator_id:int = Depends(utils.confirm_author)
):
    if thumbnail:
        if thumbnail.content_type not in ["image/jpeg", "image/png"]:
            raise UploadFormatException(
                file_name=thumbnail.filename,
                error_message="The current accepted file types are PNG and JPEG",
            )
        else:
            thumbnail = await thumbnail.read()

    # call the create_post function
    return repo.create_post(db=db, title=title, body=body, thumbnail=thumbnail, creator_id=creator_id)

# get all blog posts
@router.get(
    "/",
    summary="Get All Blog Posts",
    response_model=list[schemas.ShowBlog],
    status_code=status.HTTP_200_OK,
)
def read_all_posts(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return repo.read_all_posts(db, skip, limit)

# get single blog post
@router.get("/{post_id}", summary="Get Single Blog Post", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def read_post(*, db: Session = Depends(get_db), post_id: int):
    post = repo.read_post(db, post_id)
    return post

# update single post
@router.put("/{post_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    title: str = Form(default=None),
    body: str = Form(default=None),
    thumbnail: UploadFile | None = None,
    requester_id:int = Depends(utils.confirm_author)
):
    '''
    Perform `PUT` and `PATCH` operations.  
    When you use this endpoint, the `latest_update` field gets populated
    '''
    # ensure that changes are restricted to the author of the post
    utils.restrict_author(db, requester_id=requester_id, post_id=post_id)

    # convert the thumbnail to bytes
    if thumbnail:
        if thumbnail.content_type not in ["image/jpeg", "image/png"]:
            raise UploadFormatException(
                file_name=thumbnail.filename,
                error_message="The current accepted file types are PNG and JPEG",
            )
        else:
            thumbnail = await thumbnail.read()

    return repo.update_post(db, post_id, title, body, thumbnail)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(*,
                db: Session = Depends(get_db), 
                post_id: int,
                requester_id:int = Depends(utils.confirm_author)
                ):
    # ensure that changes are restricted to the author of the post
    utils.restrict_author(db, requester_id=requester_id, post_id=post_id)

    return repo.delete_post(db, post_id)
