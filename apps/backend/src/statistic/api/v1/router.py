from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.statistic.api.v1.endpoints.submit_feedback import (
    router as submit_feedback_router,
)
from src.statistic.api.v1.endpoints.xapi_statements import (
    router as xapi_statements_router,
)
from src.statistic.api.v1.endpoints.metric_types import (
    router as metric_types_router,
)
from src.statistic.api.v1.endpoints.student_progress import (
    router as student_progress_router,
)


router = APIRouter(
    prefix="/statistic", tags=["Statistics"], dependencies=[Depends(HTTPBearer())]
)

# Incluir todos los routers de endpoints
router.include_router(submit_feedback_router)
router.include_router(xapi_statements_router)
router.include_router(metric_types_router)
router.include_router(student_progress_router)
