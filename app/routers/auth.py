from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..utils import get_db
from .. import schemas, repo, utils

router = APIRouter(tags=['auth'])


    
@router.post('/token', response_model=schemas.Token)
def login_for_token(db:Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), is_author:bool = True):
    person = repo.resolve_login(db, form_data.username, form_data.password, is_author)
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # prefix the value of the 'sub' key with 'author:' if the is_author argument is True
    # ...else, prefix it with 'user:'
    if is_author:
        access_token = utils.create_access_token(
            data={'sub':f'author:{person.email}', 'id':person.id}
        )
    else:
        access_token = utils.create_access_token(
            data={'sub':f'user:{person.email}', 'id':person.id}
        )
    return {'access_token':access_token, 'token_type':'bearer'}

