from typing import Any, Sequence
from sqladmin import Admin, ModelView
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.shared.infrastructure.session import engine
from src.admin.auth import admin_auth_backend, verify_admin_role, load_user_with_session


class AdminAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware que carga el usuario y sesión de DB para las request del admin.
    Necesario para verificar el rol admin en cada request.
    """

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/admin"):
            result = await load_user_with_session(request)
            if result:
                user, session = result
                request.state.admin_user = user
                request.state.admin_session = session
            else:
                request.state.admin_user = None
                request.state.admin_session = None
        return await call_next(request)

from src.users.domain.user import User
from src.users.domain.professor import Professor
from src.users.domain.student import Student
from src.users.domain.teacher_settings import TeacherSettings
from src.users.domain.role import Role

from src.game.domain.game import Game
from src.game.domain.game_instance import GameInstance
from src.game.domain.segment_level import SegmentLevel
from src.game.domain.level import Level

from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment

from src.statistic.domain.progress import Progress
from src.statistic.domain.xapi_statement import XAPIStatement
from src.statistic.domain.feedback import Feedback

from src.sync.domain.sync_session import SyncSession
from src.sync.domain.sync_event import SyncEvent


class BaseAdminModelView(ModelView):
    """
    Base ModelView que verifica el rol admin en cada request.
    Solo permite acceso a usuarios con rol 'admin'.
    """

    async def _check_admin_role(self, request: Request) -> bool:
        """Verifica si el usuario actual tiene rol de admin."""
        session = request.state.admin_session
        if not session:
            return False
        
        user = request.state.admin_user
        if not user:
            return False

        return await verify_admin_role(user, session)

    async def list(self, request: Request) -> Any:
        """Override list para verificar rol admin."""
        if not await self._check_admin_role(request):
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=403,
                content={"detail": "Acceso denegado. Se requiere rol de admin."}
            )
        return await super().list(request)

    async def detail(self, request: Request, pk: Any) -> Any:
        """Override detail para verificar rol admin."""
        if not await self._check_admin_role(request):
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=403,
                content={"detail": "Acceso denegado. Se requiere rol de admin."}
            )
        return await super().detail(request, pk)

    async def insert(self, request: Request) -> Any:
        """Override insert para verificar rol admin."""
        if not await self._check_admin_role(request):
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=403,
                content={"detail": "Acceso denegado. Se requiere rol de admin."}
            )
        return await super().insert(request)

    async def edit(self, request: Request, pk: Any) -> Any:
        """Override edit para verificar rol admin."""
        if not await self._check_admin_role(request):
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=403,
                content={"detail": "Acceso denegado. Se requiere rol de admin."}
            )
        return await super().edit(request, pk)

    async def delete(self, request: Request, pk: Any) -> Any:
        """Override delete para verificar rol admin."""
        if not await self._check_admin_role(request):
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=403,
                content={"detail": "Acceso denegado. Se requiere rol de admin."}
            )
        return await super().delete(request, pk)


class UserAdminView(BaseAdminModelView, model=User):
    """AdminView para el modelo User."""
    name = "Usuario"
    name_plural = "Usuarios"
    icon = "fa-solid fa-user"
    
    column_list = [
        User.id, User.username, User.name, User.lastname, 
        User.email, User.is_active, User.role_id
    ]
    column_details_list = [
        User.id, User.username, User.name, User.lastname, 
        User.email, User.avatar_url, User.is_active, 
        User.last_login, User.role_id, User.lms_id
    ]
    column_formatters = {User.hashed_password: lambda m, c: "***"}
    form_excluded_columns = [User.hashed_password]
    
    can_edit = True
    can_create = True
    can_delete = True


class RoleAdminView(BaseAdminModelView, model=Role):
    """AdminView para el modelo Role."""
    name = "Rol"
    name_plural = "Roles"
    icon = "fa-solid fa-user-shield"
    
    column_list = [Role.id, Role.role_name, Role.description]
    column_details_list = [Role.id, Role.role_name, Role.description]
    
    can_edit = True
    can_create = True
    can_delete = True


class ProfessorAdminView(BaseAdminModelView, model=Professor):
    """AdminView para el modelo Professor."""
    name = "Profesor"
    name_plural = "Profesores"
    icon = "fa-solid fa-chalkboard-teacher"
    
    column_list = [Professor.id, Professor.user_id, Professor.department, Professor.contact_phone]
    column_details_list = [Professor.id, Professor.user_id, Professor.department, Professor.contact_phone]
    
    can_edit = True
    can_create = True
    can_delete = True


class StudentAdminView(BaseAdminModelView, model=Student):
    """AdminView para el modelo Student."""
    name = "Estudiante"
    name_plural = "Estudiantes"
    icon = "fa-solid fa-graduation-cap"
    
    column_list = [Student.id, Student.user_id, Student.last_active_at, Student.current_streak_days, Student.active_today]
    column_details_list = [Student.id, Student.user_id, Student.last_active_at, Student.current_streak_days, Student.active_today]
    
    can_edit = True
    can_create = True
    can_delete = True


class TeacherSettingsAdminView(BaseAdminModelView, model=TeacherSettings):
    """AdminView para el modelo TeacherSettings."""
    name = "Configuración de Profesor"
    name_plural = "Configuraciones de Profesor"
    icon = "fa-solid fa-cog"
    
    column_list = [
        TeacherSettings.id, TeacherSettings.user_id, 
        TeacherSettings.theme, TeacherSettings.notifications_enabled,
        TeacherSettings.interface_language
    ]
    column_details_list = [
        TeacherSettings.id, TeacherSettings.user_id, TeacherSettings.theme,
        TeacherSettings.notifications_enabled, TeacherSettings.notification_frequency,
        TeacherSettings.interface_language, TeacherSettings.auto_logout,
        TeacherSettings.session_duration_minutes, TeacherSettings.remember_login,
        TeacherSettings.color_theme, TeacherSettings.animations_enabled,
        TeacherSettings.email_notifications, TeacherSettings.date_format, TeacherSettings.timezone
    ]
    
    can_edit = True
    can_create = True
    can_delete = True


class GameAdminView(BaseAdminModelView, model=Game):
    """AdminView para el modelo Game."""
    name = "Juego"
    name_plural = "Juegos"
    icon = "fa-solid fa-gamepad"
    
    column_list = [Game.id, Game.title, Game.creator, Game.subject, Game.publication_status]
    column_details_list = [Game.id, Game.title, Game.description, Game.creator, Game.subject, Game.publication_status]
    
    # Exclude relationships from form - they should be created separately
    # Use string names to avoid issues with SQLAlchemy relationship objects
    form_excluded_columns = ["levels", "instances", "feedbacks"]
    
    can_edit = True
    can_create = True
    can_delete = True


class GameInstanceAdminView(BaseAdminModelView, model=GameInstance):
    """AdminView para el modelo GameInstance."""
    name = "Instancia de Juego"
    name_plural = "Instancias de Juego"
    icon = "fa-solid fa-play"
    
    column_list = [GameInstance.id, GameInstance.game_id, GameInstance.student_id, GameInstance.status]
    column_details_list = [GameInstance.id, GameInstance.game_id, GameInstance.student_id, GameInstance.started_at, GameInstance.ended_at, GameInstance.status]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["student", "game", "sync_sessions"]
    
    can_edit = True
    can_create = True
    can_delete = True


class SegmentLevelAdminView(BaseAdminModelView, model=SegmentLevel):
    """AdminView para el modelo SegmentLevel."""
    name = "Nivel de Segmento"
    name_plural = "Niveles de Segmento"
    icon = "fa-solid fa-layer-group"
    
    column_list = [SegmentLevel.id, SegmentLevel.level_number_id, SegmentLevel.configuration]
    column_details_list = [SegmentLevel.id, SegmentLevel.level_number_id, SegmentLevel.configuration]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["level", "progresses"]
    
    can_edit = True
    can_create = True
    can_delete = True


class LevelAdminView(BaseAdminModelView, model=Level):
    """AdminView para el modelo Level."""
    name = "Nivel"
    name_plural = "Niveles"
    icon = "fa-solid fa-list-ol"
    
    column_list = [Level.id, Level.title, Level.game_id, Level.level_number]
    column_details_list = [Level.id, Level.title, Level.game_id, Level.level_number, Level.description, Level.goal]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["game", "segments", "feedbacks"]
    
    can_edit = True
    can_create = True
    can_delete = True


class CourseAdminView(BaseAdminModelView, model=Course):
    """AdminView para el modelo Course."""
    name = "Curso"
    name_plural = "Cursos"
    icon = "fa-solid fa-book"
    
    column_list = [Course.id, Course.name, Course.school_year, Course.period_label, Course.is_active]
    column_details_list = [Course.id, Course.name, Course.description, Course.school_year, Course.period_label, Course.start_date, Course.end_date, Course.is_active]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["enrollments", "course_professors"]
    
    can_edit = True
    can_create = True
    can_delete = True


class CourseEnrollmentAdminView(BaseAdminModelView, model=CourseEnrollment):
    """AdminView para el modelo CourseEnrollment."""
    name = "Inscripción"
    name_plural = "Inscripciones"
    icon = "fa-solid fa-user-plus"
    
    column_list = [CourseEnrollment.id, CourseEnrollment.student_id, CourseEnrollment.course_id, CourseEnrollment.enrolled_at]
    column_details_list = [CourseEnrollment.id, CourseEnrollment.student_id, CourseEnrollment.course_id, CourseEnrollment.enrolled_at]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["student", "course"]
    
    can_edit = True
    can_create = True
    can_delete = True


class ProgressAdminView(BaseAdminModelView, model=Progress):
    """AdminView para el modelo Progress."""
    name = "Progreso"
    name_plural = "Progresos"
    icon = "fa-solid fa-chart-line"
    
    column_list = [Progress.id, Progress.student_id, Progress.segment_level_id, Progress.attempt_count, Progress.efficiency_rating]
    column_details_list = [
        Progress.id, Progress.student_id, Progress.segment_level_id,
        Progress.attempt_count, Progress.error_count, Progress.hints_used_count,
        Progress.errors_details, Progress.objectives_completed, Progress.efficiency_rating
    ]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["student", "segment_level"]
    
    can_edit = True
    can_create = True
    can_delete = True


class XAPIStatementAdminView(BaseAdminModelView, model=XAPIStatement):
    """AdminView para el modelo XAPIStatement."""
    name = "Declaración xAPI"
    name_plural = "Declaraciones xAPI"
    icon = "fa-solid fa-file-alt"
    
    column_list = [XAPIStatement.id, XAPIStatement.student_id, XAPIStatement.verb_id, XAPIStatement.timestamp]
    column_details_list = [
        XAPIStatement.id, XAPIStatement.student_id, XAPIStatement.verb_id,
        XAPIStatement.verb_display, XAPIStatement.object_id, XAPIStatement.object_type,
        XAPIStatement.platform, XAPIStatement.language, XAPIStatement.timestamp,
        XAPIStatement.stored, XAPIStatement.statement
    ]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["student"]
    
    can_edit = True
    can_create = True
    can_delete = True


class FeedbackAdminView(BaseAdminModelView, model=Feedback):
    """AdminView para el modelo Feedback."""
    name = "Feedback"
    name_plural = "Feedbacks"
    icon = "fa-solid fa-comment"
    
    column_list = [Feedback.id, Feedback.student_id, Feedback.game_id, Feedback.rating]
    column_details_list = [
        Feedback.id, Feedback.student_id, Feedback.professor_id, Feedback.game_id,
        Feedback.level_id, Feedback.rating, Feedback.comments
    ]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["student", "professor", "game", "level"]
    
    can_edit = True
    can_create = True
    can_delete = True


class SyncSessionAdminView(BaseAdminModelView, model=SyncSession):
    """AdminView para el modelo SyncSession."""
    name = "Sesión de Sincronización"
    name_plural = "Sesiones de Sincronización"
    icon = "fa-solid fa-sync"
    
    column_list = [SyncSession.id, SyncSession.instance_id, SyncSession.status, SyncSession.start_time]
    column_details_list = [
        SyncSession.id, SyncSession.instance_id, SyncSession.status,
        SyncSession.start_time, SyncSession.end_time
    ]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["game_instance", "events"]
    
    can_edit = True
    can_create = True
    can_delete = True


class SyncEventAdminView(BaseAdminModelView, model=SyncEvent):
    """AdminView para el modelo SyncEvent."""
    name = "Evento de Sincronización"
    name_plural = "Eventos de Sincronización"
    icon = "fa-solid fa-bolt"
    
    column_list = [SyncEvent.id, SyncEvent.sync_session_id, SyncEvent.event_type, SyncEvent.status, SyncEvent.timestamp]
    column_details_list = [
        SyncEvent.id, SyncEvent.sync_session_id, SyncEvent.event_type, SyncEvent.payload,
        SyncEvent.status, SyncEvent.timestamp
    ]
    
    # Exclude relationships from form - they should be created separately
    form_excluded_columns = ["sync_session"]
    
    can_edit = True
    can_create = True
    can_delete = True


def setup_admin(app: Any) -> Admin:
    """
    Configura SQLAdmin con todos los modelos y autenticación.
    """
    admin = Admin(
        app=app,
        engine=engine,
        title="Admin - Hello World",
        base_url="/admin",
    )

    # Los modelos están definidos en cada clase vía `model=Modelo`
    admin.add_view(UserAdminView)
    admin.add_view(RoleAdminView)
    admin.add_view(ProfessorAdminView)
    admin.add_view(StudentAdminView)
    admin.add_view(TeacherSettingsAdminView)

    admin.add_view(GameAdminView)
    admin.add_view(GameInstanceAdminView)
    admin.add_view(SegmentLevelAdminView)
    admin.add_view(LevelAdminView)

    admin.add_view(CourseAdminView)
    admin.add_view(CourseEnrollmentAdminView)

    admin.add_view(ProgressAdminView)
    admin.add_view(XAPIStatementAdminView)
    admin.add_view(FeedbackAdminView)

    admin.add_view(SyncSessionAdminView)
    admin.add_view(SyncEventAdminView)

    return admin