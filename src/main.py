from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from src.authentication.authentication import PasswordEncoder
from src.authentication.jwt import JwtEncoder
from src.db import models, storage
from src.db.config import engine, SessionLocal
from src.dto.dtos import PaginatedEntityList
from src.dto.enums import UserRole
from src.dto.schemas import User, UserWithSensitiveData, UserAuthenticationResponse, UserAuthenticationRequest, CoefficientSetup, \
    CalculationResult

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_any_authentication(request: Request) -> User:
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    try:
        jwt_enconder = JwtEncoder()
        return jwt_enconder.decode(auth_token)
    except:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

def require_admin_authorization(request: Request) -> User:
    user = require_any_authentication(request)
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    return user


def require_researcher_authorization(request: Request) -> User:
    user = require_any_authentication(request)
    if user.role != UserRole.RESEARCHER:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    return user


@app.get("/users/", response_model=PaginatedEntityList[User])
async def get_user_list(page: int = 1, page_size: int = 10, db_session: Session = Depends(get_db_session), admin: User = Depends(require_admin_authorization)):
    users = storage.get_user_list(db_session, page, page_size)
    return users

@app.post("/users/")
async def save_user(user: UserWithSensitiveData, db_session: Session = Depends(get_db_session), admin: User = Depends(require_admin_authorization)):
    existing_user = storage.get_user_by_email(db_session, user.email)
    if existing_user is not None and user.id is None:
        raise HTTPException(status_code=400, detail="User already exists")

    storage.save_user(db_session, user)

@app.get("/users/{user_id}/", response_model=User)
async def get_user_by_id(user_id: int, db_session: Session = Depends(get_db_session), admin: User = Depends(require_admin_authorization)):
    user = storage.get_user_by_id(db_session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exists")

    return user

@app.post("/auth/login/")
async def authenticate_user(request: UserAuthenticationRequest, db_session: Session = Depends(get_db_session)):
    user = storage.get_user_by_email(db_session, request.email)

    if not user:
        raise HTTPException(status_code=403, detail="Incorrect email or password")

    password_encoder = PasswordEncoder()
    if not password_encoder.is_valid(user.password, request.password):
        raise HTTPException(status_code=403, detail="Incorrect email or password")

    jwt_encoder = JwtEncoder()
    token = jwt_encoder.encode(user)
    return UserAuthenticationResponse(auth_token=token)

@app.get("/coefficient_setups/", response_model=PaginatedEntityList[CoefficientSetup])
async def get_coefficient_setup_list(page: int = 1, page_size: int = 10, db_session: Session = Depends(get_db_session), user: User = Depends(require_researcher_authorization)):
    return storage.get_coefficient_setup_list(db_session, page, page_size)

@app.get("/coefficient_setups/{id}/", response_model=CoefficientSetup)
async def get_coefficient_setup_by_id(id: int, db_session: Session = Depends(get_db_session), user: User = Depends(require_researcher_authorization)):
    coefficient_setup = storage.get_coefficient_setup_by_id(db_session, id)
    if coefficient_setup is None:
        raise HTTPException(status_code=404, detail="Coefficient Setup does not exist")

    return coefficient_setup

@app.post("/coefficient_setups/")
async def save_coefficient_setup(request: CoefficientSetup, db_session: Session = Depends(get_db_session), user: User = Depends(require_researcher_authorization)):
    request.user_id = user.id
    storage.save_coefficient_setup(db_session, request)
@app.post("/coefficient_setups/{id}/calculate/")
async def save_coefficient_setup(id: int, db_session: Session = Depends(get_db_session), user: User = Depends(require_researcher_authorization)):
    coefficient_setup = storage.get_coefficient_setup_by_id(db_session, id)
    if coefficient_setup is None:
        raise HTTPException(status_code=404, detail="Coefficient Setup does not exist")

    calculation_result = CalculationResult(**(coefficient_setup.__dict__ | {"t1": 1, "t2": 1, "s": 1, "calculated_at": datetime.now()}))
    storage.save_calculation_result(db_session, calculation_result)

    return calculation_result

@app.get("/calculation_results/", response_model=PaginatedEntityList[CalculationResult])
async def get_calculation_result_list(page: int = 1, page_size: int = 10, db_session: Session = Depends(get_db_session), user: User = Depends(require_researcher_authorization)):
    return storage.get_calculation_result_list(db_session, page, page_size)