This is a test for howdy challenge
app/
├── main.py
├── models.py # Modelo SQLAlchemy para Task (id, title, description, status)
├── schemas.py # Esquemas Pydantic (TaskCreate, TaskResponse, etc.)
├── repository.py # Métodos DB (get_task, create_task, list_tasks)
└── routes/
└── tasks.py # Rutas API
