from fastapi import APIRouter
from src.course.api.v1.endpoints.course_reports import router as course_reports_router

router = APIRouter()
router.include_router(course_reports_router)
