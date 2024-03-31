from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_zero.database import get_session
from fast_api_zero.models import User
from fast_api_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_api_zero.security import get_current_user, get_password_hash

CurrentSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session: CurrentSession):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, email=user.email, password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=200, response_model=UserList)
def read_users(session: CurrentSession, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.get('/{user_id}', status_code=200, response_model=UserPublic)
def read_user(user_id: int, session: CurrentSession):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    return db_user


@router.put('/{user_id}', status_code=200, response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: CurrentSession,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', status_code=200, response_model=Message)
def delete_user(
    user_id: int,
    session: CurrentSession,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
