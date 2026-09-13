from fastapi import FastAPI

from app.routes.tasks import router as tasks_router


app = FastAPI()
app.include_router(tasks_router)
