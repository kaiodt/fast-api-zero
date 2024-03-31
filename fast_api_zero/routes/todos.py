from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_zero.database import get_session
from fast_api_zero.models import Todo, User
from fast_api_zero.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fast_api_zero.security import get_current_user

CurrentSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', status_code=201, response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: CurrentSession,
):
    db_todo: Todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', status_code=200, response_model=TodoList)
def list_todos(
    session: CurrentSession,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: str = Query(None),
    limit: str = Query(None),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.patch('/{todo_id}', status_code=200, response_model=TodoPublic)
def patch_todo(
    todo_id: int, session: CurrentSession, user: CurrentUser, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(status_code=404, detail='Task not found')

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', status_code=200, response_model=Message)
def delete_todo(todo_id: int, session: CurrentSession, user: CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(status_code=404, detail='Task not found')

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully'}
