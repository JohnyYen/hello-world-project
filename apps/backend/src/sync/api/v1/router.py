from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.sync.api.v1.endpoints.register_sync_event import (
    router as register_sync_event_router,
)
from src.sync.api.v1.endpoints.list_sync_events import router as list_sync_events_router
from src.sync.api.v1.endpoints.start_sync_session import (
    router as start_sync_session_router,
)
from src.sync.api.v1.endpoints.end_sync_session import router as end_sync_session_router
from src.sync.api.v1.endpoints.get_sessions_by_instance import (
    router as get_sessions_by_instance_router,
)


router = APIRouter(prefix="/sync", tags=["Sync"], dependencies=[Depends(HTTPBearer())])

# Incluir todos los routers de endpoints
router.include_router(register_sync_event_router)
router.include_router(list_sync_events_router)
router.include_router(start_sync_session_router)
router.include_router(end_sync_session_router)
router.include_router(get_sessions_by_instance_router)
