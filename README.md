# Task Management API

A FastAPI service for creating, listing, completing, and deleting tasks. Tasks are stored in a local SQLite database named `tasks.db`.

## Features

- Create tasks with a unique title.
- List all tasks or filter them by priority.
- Complete a task exactly once.
- Delete tasks by ID.
- Interactive API documentation through Swagger UI and ReDoc.

## Requirements

- Python 3.12 or newer

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the API

From the project root, start the development server:

```powershell
python -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Create a task

`POST /tasks`

Request body:

```json
{
  "title": "Prepare report",
  "description": "Send the monthly report",
  "status": "pending",
  "priority": "HIGH"
}
```

`priority` accepts `LOW`, `MEDIUM`, or `HIGH`. It defaults to `MEDIUM`. The response status is `201 Created`.

```powershell
curl.exe -X POST http://127.0.0.1:8000/tasks `
	-H "Content-Type: application/json" `
	-d '{"title":"Prepare report","description":"Send the monthly report","priority":"HIGH"}'
```

Task titles must be unique. A duplicate title returns `409 Conflict` with the message `Task title already exists`.

### List tasks

`GET /tasks`

Optionally filter by priority:

```powershell
curl.exe "http://127.0.0.1:8000/tasks?priority=HIGH"
```

### Complete a task

`PATCH /tasks/{task_id}/complete`

Changes the task status to `COMPLETED`. If the task is already completed, the API returns `400 Bad Request` with `Task is already completed`. A missing task returns `404 Not Found`.

```powershell
curl.exe -X PATCH http://127.0.0.1:8000/tasks/1/complete
```

### Delete a task

`DELETE /tasks/{task_id}`

Deletes the task and returns `204 No Content`. A missing task returns `404 Not Found`.

```powershell
curl.exe -X DELETE http://127.0.0.1:8000/tasks/1
```

## Task Fields

| Field         | Type           | Default   | Notes                                      |
| ------------- | -------------- | --------- | ------------------------------------------ |
| `id`          | integer        | Generated | Database identifier                        |
| `title`       | string         | Required  | Must be unique                             |
| `description` | string or null | `null`    | Optional details                           |
| `status`      | string         | `pending` | Completion endpoint sets it to `COMPLETED` |
| `priority`    | enum           | `MEDIUM`  | `LOW`, `MEDIUM`, or `HIGH`                 |

## Tests

Run the unit tests:

```powershell
python -m pytest -q
```

Run the tests with coverage:

```powershell
python -m pytest --cov=app --cov-report=term-missing -q
```

## Project Structure

```text
app/
├── main.py              # FastAPI application
├── enums.py             # Shared Priority enum
├── models.py            # SQLAlchemy Task model
├── schemas.py           # Pydantic request and response schemas
├── repository.py        # Database session and persistence operations
└── routes/
		└── tasks.py         # Task API endpoints
tests/
└── test_tasks.py        # Unit tests for task operations
```
