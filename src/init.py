from src.db import storage
from src.dto.enums import UserRole
from src.dto.schemas import UserWithSensitiveData
from src.main import get_db_session

db_session = next(get_db_session())
user = UserWithSensitiveData(id=None, email="admin@test.com", password="admin", role=UserRole.ADMIN)
storage.save_user(db_session, user)