from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.dto.enums import UserRole


class User(BaseModel):
    model_config = {"from_attributes": True}

    id: Optional[int]
    email: str
    role: UserRole

class UserWithSensitiveData(User):
    password: Optional[str]

class CoefficientSetup(BaseModel):
    model_config = {"from_attributes": True}

    id: Optional[int]
    user_id: Optional[int]
    alpha: float
    beta: float
    mu: float
    g: float
    a: float
    n: float

class CalculationResult(BaseModel):
    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}

    id: int
    user_id: int
    calculated_at: datetime
    alpha: float
    beta: float
    mu: float
    g: float
    a: float
    n: float
    t1: float
    t2: float
    s: float

class UserAuthenticationRequest(BaseModel):
    email: str
    password: str

class UserAuthenticationResponse(BaseModel):
    auth_token: str