from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from app.utils.mixin import UserMixin
from database import Base
from sqlalchemy.orm import relationship
from app.projects.models import Project


class User(SQLAlchemyBaseUserTable[int], Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    projects = relationship(Project, back_populates="user")
