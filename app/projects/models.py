from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_utils.types.url import URLType
from sqlalchemy.orm import relationship
from app.utils.mixin import UserMixin
from database import Base


class Project(Base, UserMixin):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="projects")
    image = relationship("Image", back_populates="project")


class Image(Base, UserMixin):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True)
    url = Column(URLType, nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id))
    project = relationship("Project", back_populates="image")
    
    
    