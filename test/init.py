from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.authentication.jwt import JwtEncoder
from src.db import storage
from src.db.config import Base
from src.dto.enums import UserRole
from src.dto.schemas import UserWithSensitiveData
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
admin_user = UserWithSensitiveData(id=None, email="admin@test.com", password="qwe", role=UserRole.ADMIN)
admin_user = storage.save_user(db_session, admin_user)
admin_jwt_token = jwt_encoder.encode(admin_user)
admin_auth_headers = {"Authorization": f"{admin_jwt_token}"}

researcher_user = UserWithSensitiveData(id=None, email="researcher@test.com", password="qwe", role=UserRole.RESEARCHER)
researcher_user = storage.save_user(db_session, researcher_user)
researcher_jwt_token = jwt_encoder.encode(researcher_user)
researcher_auth_headers = {"Authorization": f"{researcher_jwt_token}"}