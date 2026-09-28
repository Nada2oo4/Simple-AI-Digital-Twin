from app.models import DigitalTwin, Task


def get_tasks(digital_twin: DigitalTwin):
    """Get all current tasks for the user."""
    return digital_twin.tasks


def add_task(
    digital_twin: DigitalTwin,
    title: str,
    priority: str,
    deadline: str | None = None
):
    """Add a new task to the user's task list."""

    new_task = Task(
        id=len(digital_twin.tasks) + 1,
        title=title,
        priority=priority,
        deadline=deadline
    )

    digital_twin.tasks.append(new_task)

    return new_task


def update_task(
    digital_twin: DigitalTwin,
    task_id: int,
    status: str
):
    """Update the status of an existing task."""

    for task in digital_twin.tasks:
        if task.id == task_id:
            task.status = status
            return task

    return None