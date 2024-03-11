from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.authentication.jwt import JwtEncoder
from src.db import storage
from src.db.config import Base
from src.db.storage import get_user_by_email
from src.dto.enums import UserRole
from src.dto.schemas import User, ChangeUser
from src.main import app, get_db_session

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:pwd@localhost:5432/tests"
engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db_session_override():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_session] = get_db_session_override
db_session = next(get_db_session_override())

client = TestClient(app)

jwt_encoder = JwtEncoder()
admin_user = ChangeUser(id=None, email="admin@test.com", password="qwe", role=UserRole.ADMIN)
admin_user = storage.save_user(db_session, admin_user)
admin_jwt_token = jwt_encoder.encode(admin_user)
admin_auth_headers = {"Authorization": f"{admin_jwt_token}"}

researcher_user = ChangeUser(id=None, email="researcher@test.com", password="qwe", role=UserRole.RESEARCHER)
researcher_user = storage.save_user(db_session, researcher_user)
researcher_jwt_token = jwt_encoder.encode(researcher_user)
researcher_auth_headers = {"Authorization": f"{researcher_jwt_token}"}


def test_create_user():
    response = client.post("/users/", json={"id": None, "email": "lehadnk@gmail.com", "password": "qwe", "role": UserRole.ADMIN.value})
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