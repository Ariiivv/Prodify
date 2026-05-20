from fastapi import APIRouter

from app.api import (
    analytics,
    health,
    sessions,
    tasks,
    users,
    work_items,
    workspaces,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(workspaces.router)
api_router.include_router(work_items.router)
api_router.include_router(tasks.router)
api_router.include_router(sessions.router)
api_router.include_router(analytics.router)
