from collections.abc import Generator

from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base, Priority, Task
from app.schemas import TaskCreate


engine = create_engine("sqlite:///./tasks.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:

	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def list_tasks(db: Session, priority: Priority | None = None) -> list[Task]:

	statement = select(Task)
	if priority is not None:
		statement = statement.where(Task.priority == priority)
	return list(db.scalars(statement).all())


def create_task(db: Session, task_data: TaskCreate) -> Task:
	existing_task = db.scalar(select(Task).where(Task.title == task_data.title))
	if existing_task is not None:
		raise ValueError("Task title already exists")

	task = Task(
		title=task_data.title,
		description=task_data.description,
		status=task_data.status,
		priority=Priority(task_data.priority.value),
	)
	db.add(task)
	try:
		db.commit()
	except IntegrityError as error:
		db.rollback()
		raise ValueError("Task title already exists") from error
	db.refresh(task)
	return task
