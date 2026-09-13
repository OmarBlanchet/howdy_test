from pydantic import BaseModel, ConfigDict

from app.enums import Priority



class TaskBase(BaseModel):
	title: str
	description: str | None = None
	status: str = "pending"
	priority: Priority = Priority.MEDIUM


class TaskCreate(TaskBase):
	pass


class TaskResponse(TaskBase):
	id: int

	model_config = ConfigDict(from_attributes=True)
