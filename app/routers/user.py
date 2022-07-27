from fastapi import APIRouter, Depends, status, Form
from .. import repo, utils, schemas
from sqlalchemy.orm import Session

get_db = utils.get_db

router = APIRouter(
    tags=['user'],
    prefix='/user',
)

@router.post('/{id}', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(*, user:schemas.PersonCreate, db:Session = Depends(get_db), receive_mails:bool = False):
    # deal with user wanting to receive mails
    return repo.create_person(db, user)

@router.get('/', summary='Get All Users', response_model=list[schemas.User], status_code=status.HTTP_200_OK)
def get_users(*, db:Session = Depends(get_db), skip:int = 0, limit:int = 100):
    return repo.read_persons(db, skip, limit)

@router.get('/{id}', response_model=schemas.User, status_code=status.HTTP_200_OK)
def get_user(*, db:Session = Depends(get_db), id:int):
    user = repo.read_person(db, id)
    return user

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(
    *,
    db: Session = Depends(get_db),
    id: int,
    name: str = Form(default=None),
    email: str = Form(default=None)
):
    changed_email, value = repo.update_person(db, id, name, email)
    if changed_email:
        # add background task to send mail to new email
        ...
    return value