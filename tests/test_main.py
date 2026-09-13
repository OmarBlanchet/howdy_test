from app.main import app


def test_application_registers_task_routes():
    paths = set(app.openapi()["paths"])

    assert paths == {
        "/tasks",
        "/tasks/{task_id}/complete",
        "/tasks/{task_id}",
    }