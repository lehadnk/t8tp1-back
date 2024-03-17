import math
from typing import Optional
import bcrypt
from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.authentication.authentication import PasswordEncoder
from src.db.models import User, CoefficientSetup, CalculationResult
from src.dto.schemas import User as UserDto, UserWithSensitiveData
from src.dto.schemas import CoefficientSetup as CoefficientSetupDto
from src.dto.schemas import CalculationResult as CalculationResultDto
from src.dto.dtos import PaginatedEntityList


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.query(User).filter(User.id == user_id).first()

def get_user_by_email(session: Session, email: str) -> Optional[UserWithSensitiveData]:
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None

    return UserWithSensitiveData(**user.__dict__)

def get_user_list(session: Session, page: int, page_size: int) -> PaginatedEntityList[UserDto]:
    offset = (page - 1) * page_size
    query = session.query(User)
    users = [UserDto(**u.__dict__) for u in query.order_by("id").offset(offset).limit(page_size).all()]
    users_count = query.count()

    return PaginatedEntityList[UserDto](items=users, total=users_count, page=page, page_size=page_size, pages=math.ceil(users_count / page_size))

def save_user(session: Session, user_dto: UserWithSensitiveData) -> UserDto:
    if user_dto.password is not None:
        password_encoder = PasswordEncoder()
        user_dto.password = password_encoder.encode(user_dto.password)

    if user_dto.id is not None:
        user = get_user_by_id(session, user_dto.id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in user_dto.dict().items():
            if key != 'password' or user_dto.password is not None:
                setattr(user, key, value)
    else:
        user = User(**user_dto.dict())

    session.add(user)
    session.commit()
    session.refresh(user)
    return UserDto(**user.__dict__)

def get_coefficient_setup_list(session: Session, page: int, page_size: int) -> PaginatedEntityList[CoefficientSetupDto]:
    offset = (page - 1) * page_size
    query = session.query(CoefficientSetup)
    coefficient_setups = [CoefficientSetupDto(**cs.__dict__) for cs in query.offset(offset).limit(page_size).all()]
    coefficient_setup_count = query.count()

    return PaginatedEntityList[CoefficientSetupDto](items=coefficient_setups, total=coefficient_setup_count, page=page, page_size=page_size, pages=math.ceil(coefficient_setup_count / page_size))

def save_coefficient_setup(session: Session, coefficient_setup_dto: CoefficientSetupDto):
    db_model = CoefficientSetup(**coefficient_setup_dto.dict())
    session.add(db_model)
    session.commit()

def delete_coefficient_setup(session: Session, coefficient_setup_id: int):
    session.query(CoefficientSetup).filter(CoefficientSetup.id == coefficient_setup_id).delete()

def get_coefficient_setup_by_id(session: Session, coefficient_setup_id: int) -> CoefficientSetup:
    return session.query(CoefficientSetup).filter(CoefficientSetup.id == coefficient_setup_id).first()

def get_calculation_result_list(session: Session, page: int, page_size: int) -> PaginatedEntityList[CalculationResultDto]:
    offset = (page - 1) * page_size
    query = session.query(CalculationResult)
    coefficient_setups = [CalculationResultDto(**cr.__dict__) for cr in query.offset(offset).limit(page_size).all()]
    coefficient_setup_count = query.count()

    return PaginatedEntityList[CalculationResultDto](items=coefficient_setups, total=coefficient_setup_count, page=page, page_size=page_size, pages=math.ceil(coefficient_setup_count / page_size))

def save_calculation_result(session: Session, calculation_result_dto: CalculationResultDto):
    db_model = CalculationResult(**calculation_result_dto.dict())
    session.add(db_model)
    session.commit()


def get_calculation_result_by_id(session: Session, id: int) -> CalculationResult:
    return session.query(CalculationResult).filter(CalculationResult.id == id).first()