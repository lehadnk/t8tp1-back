from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'admin'
    RESEARCHER = 'researcher'