<<<<<<< HEAD
from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment

__all__ = ["Course", "CourseEnrollment"]
=======
from .course import Course
from .course_professor import CourseProfessor
from .course_enrollment import CourseEnrollment

__all__ = [
    "Course",
    "CourseProfessor",
    "CourseEnrollment",
]
>>>>>>> develop
