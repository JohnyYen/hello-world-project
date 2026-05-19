# Game Domain Models
from src.game.domain import Game, GameInstance, SegmentLevel, Level

# User Domain Models
from src.users.domain import User, Professor, Student, TeacherSettings, Role
from src.users.domain.notification import Notification  # noqa: F401 - Required by User model relationship

# Statistic Domain Models
from src.statistic.domain import Feedback, MetricType, Progress, XAPIStatement

# Sync Domain Models
from src.sync.domain import SyncSession, SyncEvent

# Course Domain Models
from src.course.domain import Course, CourseEnrollment
