from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.users.api.v1.endpoints.create_user import router as create_user_router
from src.users.api.v1.endpoints.get_users import router as get_users_router
from src.users.api.v1.endpoints.get_professor_profile import (
    router as get_professor_profile_router,
)
from src.users.api.v1.endpoints.update_professor_profile import (
    router as update_professor_profile_router,
)
from src.users.api.v1.endpoints.get_professor_settings import (
    router as get_professor_settings_router,
)
from src.users.api.v1.endpoints.update_professor_settings import (
    router as update_professor_settings_router,
)
from src.users.api.v1.endpoints.list_students import router as list_students_router
from src.users.api.v1.endpoints.get_student_detail import (
    router as get_student_detail_router,
)
from src.users.api.v1.endpoints.create_student import router as create_student_router
from src.users.api.v1.endpoints.update_student import router as update_student_router
from src.users.api.v1.endpoints.delete_student import router as delete_student_router
from src.users.api.v1.endpoints.get_student_progress import (
    router as get_student_progress_router,
)
from src.users.api.v1.endpoints.get_student_reports import (
    router as get_student_reports_router,
)
from src.users.api.v1.endpoints.lms_credentials import router as lms_credentials_router
from src.users.api.v1.endpoints.lms_sync import router as lms_sync_router
from src.users.api.v1.endpoints.get_user import router as get_user_router
from src.users.api.v1.endpoints.update_user import router as update_user_router
from src.users.api.v1.endpoints.delete_user import router as delete_user_router
from src.users.api.v1.endpoints.student_activity import router as student_activity_router


router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(HTTPBearer())]
)

# Incluir todos los routers de endpoints
# ORDEN IMPORTANTE: routers más específicos primero
router.include_router(list_students_router)
router.include_router(get_student_detail_router)
router.include_router(create_student_router)
router.include_router(update_student_router)
router.include_router(delete_student_router)
router.include_router(get_student_progress_router)
router.include_router(get_student_reports_router)
router.include_router(create_user_router)
router.include_router(get_users_router)
router.include_router(get_professor_profile_router)
router.include_router(update_professor_profile_router)
router.include_router(get_professor_settings_router)
router.include_router(update_professor_settings_router)
router.include_router(lms_credentials_router)
router.include_router(lms_sync_router)
router.include_router(update_user_router)
router.include_router(delete_user_router)
router.include_router(student_activity_router)
# Este debe ser el último para rutas con path params
router.include_router(get_user_router)
