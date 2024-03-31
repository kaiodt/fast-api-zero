from fast_api_zero.models import TodoState

from .conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test todo description',
        'state': 'draft',
    }


def test_list_todos(session, client, user, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 5


def test_list_todos_pagination(session, client, user, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 2


def test_list_todos_filter_title(session, client, user, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test Todo 1')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test Todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 5


def test_list_todos_filter_description(session, client, user, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5, user_id=user.id, description='Todo description'
        )
    )
    session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 5


def test_list_todos_filter_state(session, client, user, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 5


def test_list_todos_filter_combination(session, client, user, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test Todo 1',
            description='Todo description',
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test Todo 2',
            description='Other todo',
            state=TodoState.todo,
        )
    )

    session.commit()

    response = client.get(
        '/todos/?title=Test Todo 1&description=description&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 5


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'New title test'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json()['title'] == 'New title test'


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/10',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'Task has been deleted successfully'}


def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}
