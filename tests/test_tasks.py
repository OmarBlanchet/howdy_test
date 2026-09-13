import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import Base, Task
from app.routes.tasks import complete_task, delete_task, post_task
from app.schemas import TaskCreate


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_complete_task_changes_status_to_completed(db):
    task = Task(title="Finish report", status="PENDING")
    db.add(task)
    db.commit()

    completed_task = complete_task(task.id, db)

    assert completed_task.status == "COMPLETED"
    assert db.get(Task, task.id).status == "COMPLETED"


def test_complete_task_rejects_already_completed_task(db):
    task = Task(title="Finished report", status="COMPLETED")
    db.add(task)
    db.commit()

    with pytest.raises(HTTPException) as error:
        complete_task(task.id, db)

    assert error.value.status_code == 400
    assert error.value.detail == "Task is already completed"


def test_complete_task_returns_not_found_for_missing_task(db):
    with pytest.raises(HTTPException) as error:
        complete_task(999, db)

    assert error.value.status_code == 404


def test_delete_task_removes_existing_task(db):
    task = Task(title="Remove report", status="PENDING")
    db.add(task)
    db.commit()
    task_id = task.id

    delete_task(task_id, db)

    assert db.get(Task, task_id) is None


def test_delete_task_returns_not_found_for_missing_task(db):
    with pytest.raises(HTTPException) as error:
        delete_task(999, db)

    assert error.value.status_code == 404
    assert error.value.detail == "Task not found"


def test_create_task_rejects_duplicate_title(db):
    db.add(Task(title="Unique report", status="PENDING"))
    db.commit()

    with pytest.raises(HTTPException) as error:
        post_task(TaskCreate(title="Unique report"), db)

    assert error.value.status_code == 409
    assert error.value.detail == "Task title already exists"
