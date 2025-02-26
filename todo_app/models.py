from .extensions import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")


class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False, unique=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="tasks")
