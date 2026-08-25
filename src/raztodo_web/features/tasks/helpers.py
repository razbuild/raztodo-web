import os
from typing import Any

from raztodo_web.features.tasks.schemas import TaskResponse


def remove_file(path: str) -> None:
    if os.path.exists(path):
        os.unlink(path)


def task_to_response(task: Any) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=getattr(task, "description", "") or "",
        done=getattr(task, "done", False),
        created_at=getattr(task, "created_at", "") or "",
        priority=getattr(task, "priority", "") or "",
        due_date=getattr(task, "due_date", None),
        tags=list(getattr(task, "tags", None) or []),
        project=getattr(task, "project", None),
    )
