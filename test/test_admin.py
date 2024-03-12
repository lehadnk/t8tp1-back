from src.db.storage import get_user_by_email
from src.dto.enums import UserRole
from test.init import client, db_session, admin_auth_headers, researcher_auth_headers

def test_create_user():
    response = client.post("/users/", json={"id": None, "email": "lehadnk@gmail.com", "password": "qwe", "role": UserRole.ADMIN.value}, headers=admin_auth_headers)
    assert response.status_code == 200

    user = get_user_by_email(db_session, email="lehadnk@gmail.com")
    assert user is not None
    assert user.password is not None
    assert user.id is not None
    assert user.email == "lehadnk@gmail.com"
    assert user.role == UserRole.ADMIN

def test_get_user_list():
    response = client.get('/users/', headers=admin_auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert len(data['items']) == 3
    assert data['page'] == 1
    assert data['total'] == 3

def test_get_user_by_id():
    response = client.get('/users/1', headers=admin_auth_headers)
    assert response.status_code == 200

    user = response.json()
    assert user is not None
    assert user['id'] == 1

def test_accessing_user_list_with_researcher_token():
    response = client.get('/users/', headers=researcher_auth_headers)
    assert response.status_code == 403

def test_login():
    response = client.post("/auth/login/", json={"email": "lehadnk@gmail.com", "password": "qwe"})
    assert response.status_code == 200

    data = response.json()

    assert data['auth_token'] is not None

def test_incorrect_login():
    response = client.post("/auth/login/", json={"email": "lehadnk@gmail.com", "password": "asd"})
    assert response.status_code == 403