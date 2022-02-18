from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    body = Column(String, nullable=False)
    completed = Column(Boolean, nullable=True)
    username = Column(String, nullable=True)

class Users(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    pwd_hashed = Column(String, nullable=False)