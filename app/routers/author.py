from fastapi import APIRouter, Depends, Form, status
from .. import repo, utils, schemas
from sqlalchemy.orm import Session

get_db = utils.get_db

router = APIRouter(
    tags=["author"],
    prefix="/author",
)

# create
@router.post("/{id}", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_author(*, author: schemas.PersonCreate, db: Session = Depends(get_db)):
    return repo.create_person(db, author, is_author=True)


# read all
@router.get("/", summary="Get All Authors", response_model=list[schemas.Author], status_code=status.HTTP_200_OK)
def get_authors(*, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return repo.read_persons(db, skip, limit, is_author=True)


# read single
@router.get("/{id}", response_model=schemas.Author, status_code=status.HTTP_200_OK)
def get_author(*, db: Session = Depends(get_db), id: int):
    author = repo.read_person(db, id, is_author=True)
    return author


# update single
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_author(
    *,
    db: Session = Depends(get_db),
    id: int,
    name: str = Form(default=None),
    email: str = Form(default=None)
):
    changed_email, value = repo.update_person(db, id, name, email, is_author=True)
    if changed_email:
        # add background task to send mail to new email
        ...
    return value
