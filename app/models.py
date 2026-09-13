from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import declarative_base

from app.enums import Priority


Base = declarative_base()


class Task(Base):
	__tablename__ = "tasks"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, nullable=False, unique=True)
	description = Column(String, nullable=True)
	status = Column(String, nullable=False, default="pending")
	priority = Column(Enum(Priority), nullable=False, default=Priority.MEDIUM)
