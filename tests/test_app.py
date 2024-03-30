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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == 200
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_user_returns_404_when_not_found(client):
    response_negative_id = client.get('/users/-1')

    response_out_of_bound_id = client.get('/users/1000000000')

    assert response_negative_id.status_code == 404
    assert response_negative_id.json() == {'detail': 'User not found'}

    assert response_out_of_bound_id.status_code == 404
    assert response_out_of_bound_id.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
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
    response_negative_id = client.put(
        '/users/-1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    response_out_of_bound_id = client.put(
        '/users/1000000000',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_negative_id.status_code == 404
    assert response_negative_id.json() == {'detail': 'User not found'}

    assert response_out_of_bound_id.status_code == 404
    assert response_out_of_bound_id.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_returns_404_when_not_found(client):
    response_negative_id = client.delete('/users/-1')

    response_out_of_bound_id = client.delete('/users/1000000000')

    assert response_negative_id.status_code == 404
    assert response_negative_id.json() == {'detail': 'User not found'}

    assert response_out_of_bound_id.status_code == 404
    assert response_out_of_bound_id.json() == {'detail': 'User not found'}
