from datetime import datetime
from database import Base
from sqlalchemy import Column, DateTime


class UserMixin:
    data_created = Column(DateTime, default=datetime.utcnow)
    data_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)