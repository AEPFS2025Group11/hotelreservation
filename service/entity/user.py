from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SqlEnum

from app.util.base import Base
from app.util.enums import Role


@dataclass
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(Role), nullable=False)
