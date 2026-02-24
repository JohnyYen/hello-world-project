from fastapi import APIRouter

from src.statistic.api.v1.endpoints.submit_feedback import (
    router as submit_feedback_router,
)
from src.statistic.api.v1.endpoints.xapi_statements import (
    router as xapi_statements_router,
)


router = APIRouter(prefix="/statistic", tags=["Statistics"])

# Incluir todos los routers de endpoints
router.include_router(submit_feedback_router)
router.include_router(xapi_statements_router)
