from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_zero.models import Todo, User


def test_create_user(session: Session):
    new_user = User(
        username='alice', email='alice@example.com', password='secret'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_create_todo(session: Session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test todo description',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    assert todo in user.todos
