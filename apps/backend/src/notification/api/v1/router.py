"""
Notifications API v1 Router.

Aggregates all notification endpoints under /api/v1/notifications.
"""

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.notification.api.v1.endpoints.list_notifications import (
    router as list_notifications_router,
)
from src.notification.api.v1.endpoints.mark_read import (
    router as mark_read_router,
)
from src.notification.api.v1.endpoints.mark_all_read import (
    router as mark_all_read_router,
)
from src.notification.api.v1.endpoints.delete_notification import (
    router as delete_notification_router,
)

router = APIRouter(
    tags=["Notifications"],
    dependencies=[Depends(HTTPBearer())],
)

router.include_router(list_notifications_router)
router.include_router(mark_read_router)
router.include_router(mark_all_read_router)
router.include_router(delete_notification_router)
