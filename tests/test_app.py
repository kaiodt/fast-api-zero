from fast_api_zero.schemas import UserPublic


def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_returns_400_when_user_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Username already registered'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == 200
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_user_returns_404_when_not_found(client):
    response = client.get('/users/-1')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_returns_404_when_not_found(client):
    response = client.put(
        '/users/-1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_returns_404_when_not_found(client):
    response = client.delete('/users/-1')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
