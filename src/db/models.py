from sqlalchemy import Column, Integer, String, Enum as AchemyEnum, ForeignKey, Float, DateTime, func

from sqlalchemy.orm import relationship

from .config import Base
from ..dto.enums import UserRole


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(AchemyEnum(UserRole), nullable=False)

class CoefficientSetup(Base):
    __tablename__ = 'coefficient_setups'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    name = Column(String)
    alpha = Column(Float(precision=2))
    beta = Column(Float(precision=2))
    mu = Column(Float(precision=2))
    g = Column(Float(precision=2))
    a = Column(Float(precision=2))
    n = Column(Float(precision=2))

    user = relationship("User")

class CalculationResult(Base):
    __tablename__ = 'calculation_results'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    calculated_at = Column(DateTime, default=func.now())
    alpha = Column(Float(precision=2))
    beta = Column(Float(precision=2))
    mu = Column(Float(precision=2))
    g = Column(Float(precision=2))
    a = Column(Float(precision=2))
    n = Column(Float(precision=2))
    t1 = Column(Float(precision=2))
    t2 = Column(Float(precision=2))
    s = Column(Float(precision=2))