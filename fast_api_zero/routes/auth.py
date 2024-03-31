from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_zero.database import get_session
from fast_api_zero.models import User
from fast_api_zero.schemas import Token
from fast_api_zero.security import create_access_token, verify_password

CurrentSession = Annotated[Session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', status_code=200, response_model=Token)
def login_for_access_token(
    form_data: OAuth2Form,
    session: CurrentSession,
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
