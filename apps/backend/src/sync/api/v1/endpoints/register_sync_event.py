from fastapi import APIRouter, Depends, HTTPException, status

from src.sync.api.v1.schemas.sync_event import SyncEventCreate, SyncEventSchema
from src.sync.application.service.sync_event_service import SyncEventService
from src.sync.api.v1.dependencies import get_sync_event_service
from src.shared.domain.exceptions import NotFoundException
from src.shared.infrastructure.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.sync.domain.event_types import SyncEventType
from src.statistic.application.service.xapi_statement_service import (
    XAPIStatementService,
)
from src.statistic.infrastructure.xapi_statement_repository import (
    XAPIStatementRepository,
)
from src.sync.infrastructure.mapper.sync_event_to_xapi_mapper import (
    SyncEventToXAPIMapper,
)
from src.sync.application.handler.progress_updater import ProgressUpdater


router = APIRouter(prefix="/sync-events")


@router.post("", response_model=SyncEventSchema, status_code=status.HTTP_201_CREATED)
async def register_sync_event(
    sync_event: SyncEventCreate,
    service: SyncEventService = Depends(get_sync_event_service),
    db: AsyncSession = Depends(get_db),
):
    """
    Registra un evento (acción del jugador).
    """
    try:
        event = await service.create(event_data=sync_event)

        # Save event_id before processing
        event_id = int(str(event.id))

        # Classify event
        event_type = str(event.event_type)
        classification = SyncEventType.classify(event_type)

        # Process events through xAPI pipeline (complex events only)
        if classification == SyncEventType.COMPLEX:
            mapper = SyncEventToXAPIMapper(db)
            xapi_repository = XAPIStatementRepository(db)
            xapi_service = XAPIStatementService(xapi_repository)

            xapi_statement = await mapper.map(event)
            await xapi_service.save_statement(xapi_statement)

        # Update progress for ALL events (both simple and complex)
        progress_updater = ProgressUpdater(db)
        await progress_updater.update(event)

        # Update event status
        event.status = "processed"
        await db.commit()

        # Reload event to get updated status
        from src.sync.infrastructure.repositories.sync_event_repository import (
            SyncEventRepository,
        )

        repo = SyncEventRepository(db)
        updated_event = await repo.get_by_id(event_id)

        return SyncEventSchema(
            id=event_id,
            sync_session_id=int(str(updated_event.sync_session_id)),
            event_type=str(updated_event.event_type),
            payload=updated_event.payload,
            timestamp=updated_event.timestamp,
            status=str(updated_event.status),
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recurso no encontrado en sync: {str(e)}",
        )
