"""
Ownership and hierarchy validation for User → Workspace → WorkItem → Task → Session.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_or_404
from app.models.user import User
from app.models.workspace import Workspace
from app.models.work_item import WorkItem
from app.models.task import Task


def require_user(db: Session, user_id: str) -> User:
    return get_or_404(db, User, user_id, name="user")


def require_workspace_for_user(
    db: Session, workspace_id: str, user_id: str
) -> Workspace:
    workspace = get_or_404(db, Workspace, workspace_id, name="workspace")
    if workspace.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="workspace does not belong to this user",
        )
    return workspace


def require_work_item_for_user(
    db: Session, work_item_id: str, user_id: str
) -> WorkItem:
    work_item = get_or_404(db, WorkItem, work_item_id, name="work_item")
    if work_item.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="work_item does not belong to this user",
        )
    return work_item


def require_task_for_user(db: Session, task_id: str, user_id: str) -> Task:
    task = get_or_404(db, Task, task_id, name="task")
    work_item = get_or_404(db, WorkItem, task.work_item_id, name="work_item")
    if work_item.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="task does not belong to this user",
        )
    return task


def validate_work_item_ownership(
    db: Session, *, user_id: str, workspace_id: str
) -> Workspace:
    """Ensure user exists, workspace exists, and workspace is owned by user."""
    require_user(db, user_id)
    return require_workspace_for_user(db, workspace_id, user_id)
