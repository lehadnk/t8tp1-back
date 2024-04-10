from db import storage
from dto.enums import UserRole
from dto.schemas import UserWithSensitiveData
from main import get_db_session

db_session = next(get_db_session())
user = UserWithSensitiveData(id=None, email="admin@test.com", password="admin", role=UserRole.ADMIN)
storage.save_user(db_session, user)