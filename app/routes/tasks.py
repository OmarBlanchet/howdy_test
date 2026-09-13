from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models import Priority, Task
from app.repository import create_task, get_db, list_tasks
from app.schemas import TaskCreate, TaskResponse


router = APIRouter(prefix="/tasks")


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def post_task(task_data: TaskCreate, db: Session = Depends(get_db)) -> Task:
	try:
		return create_task(db, task_data)
	except ValueError as error:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail=str(error),
		) from error


@router.get("", response_model=list[TaskResponse])
def get_tasks(
	priority: Priority | None = Query(default=None),
	db: Session = Depends(get_db),
) -> list[TaskResponse]:
	return list_tasks(db, priority)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)) -> Task:
	task = db.get(Task, task_id)
	if task is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Task not found",
		)

	if task.status == "COMPLETED":
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Task is already completed",
		)

	task.status = "COMPLETED"
	db.commit()
	db.refresh(task)
	return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
	task = db.get(Task, task_id)
	if task is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Task not found",
		)

	db.delete(task)
	db.commit()
