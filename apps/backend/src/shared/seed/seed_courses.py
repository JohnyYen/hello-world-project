from src.course.domain.course import Course
from src.course.domain.course_professor import CourseProfessor
from src.course.domain.course_enrollment import CourseEnrollment
from src.shared.infrastructure.session import AsyncSession
from sqlalchemy import select


async def seed_courses(db: AsyncSession):
    """Seed courses with professors."""
    from src.users.domain.professor import Professor

    # Get professors
    professors_query = select(Professor).limit(5)
    professors = (await db.execute(professors_query)).scalars().all()

    if not professors:
        print("No professors found for courses")
        return []

    courses_data = [
        {
            "name": "Introducción a la Programación",
            "description": "Curso fundamental de programación usando Python",
            "school_year": "2024-2025",
            "period_label": "Q1",
            "start_date": "2025-01-15",
            "end_date": "2025-06-30",
            "is_active": True,
            "professor_indexes": [0],
        },
        {
            "name": "Matemáticas Discretas",
            "description": "Fundamentos matemáticos para ciencias de la computación",
            "school_year": "2024-2025",
            "period_label": "Q1",
            "start_date": "2025-01-15",
            "end_date": "2025-06-30",
            "is_active": True,
            "professor_indexes": [1],
        },
        {
            "name": "Química General",
            "description": "Introducción a los principios de la química",
            "school_year": "2024-2025",
            "period_label": "Q1",
            "start_date": "2025-01-15",
            "end_date": "2025-06-30",
            "is_active": True,
            "professor_indexes": [2],
        },
        {
            "name": "Física I",
            "description": "Mecánica clásica y termodinámica básica",
            "school_year": "2024-2025",
            "period_label": "Q1",
            "start_date": "2025-01-15",
            "end_date": "2025-06-30",
            "is_active": True,
            "professor_indexes": [3],
        },
        {
            "name": "Biología Celular",
            "description": "Estructura y función de las células",
            "school_year": "2024-2025",
            "period_label": "Q1",
            "start_date": "2025-01-15",
            "end_date": "2025-06-30",
            "is_active": True,
            "professor_indexes": [4],
        },
        {
            "name": "Estructuras de Datos",
            "description": "Algoritmos y estructuras de datos avanzadas",
            "school_year": "2024-2025",
            "period_label": "Q2",
            "start_date": "2025-07-15",
            "end_date": "2025-12-30",
            "is_active": True,
            "professor_indexes": [0, 1],
        },
        {
            "name": "Cálculo Diferencial",
            "description": "Introducción al cálculo y derivadas",
            "school_year": "2024-2025",
            "period_label": "Q2",
            "start_date": "2025-07-15",
            "end_date": "2025-12-30",
            "is_active": True,
            "professor_indexes": [1],
        },
        {
            "name": "Base de Datos",
            "description": "Diseño y gestión de sistemas de bases de datos",
            "school_year": "2024-2025",
            "period_label": "Q2",
            "start_date": "2025-07-15",
            "end_date": "2025-12-30",
            "is_active": True,
            "professor_indexes": [0],
        },
    ]

    courses = []
    for course_data in courses_data:
        # Check if course exists
        query = select(Course).where(Course.name == course_data["name"])
        existing = (await db.execute(query)).scalars().first()

        if existing:
            print(f"Course '{course_data['name']}' already exists")
            courses.append(existing)
            continue

        # Create course
        from datetime import date
        course = Course(
            name=course_data["name"],
            description=course_data["description"],
            school_year=course_data["school_year"],
            period_label=course_data["period_label"],
            start_date=date.fromisoformat(course_data["start_date"]),
            end_date=date.fromisoformat(course_data["end_date"]),
            is_active=course_data["is_active"],
        )
        db.add(course)
        await db.flush()

        # Add professors to course
        for prof_idx in course_data["professor_indexes"]:
            if prof_idx < len(professors):
                course_prof = CourseProfessor(
                    course_id=course.id,
                    professor_id=professors[prof_idx].id,
                )
                db.add(course_prof)

        courses.append(course)
        print(f"Seeded course: {course_data['name']}")

    return courses


async def seed_enrollments(db: AsyncSession):
    """Seed course enrollments for students."""
    from src.users.domain.student import Student
    from src.course.domain.course import Course

    # Get students and courses
    students_query = select(Student).limit(20)
    students = (await db.execute(students_query)).scalars().all()

    courses_query = select(Course).limit(8)
    courses = (await db.execute(courses_query)).scalars().all()

    if not students or not courses:
        print("No students or courses found for enrollments")
        return []

    import random

    enrollments = []

    for student in students:
        # Randomly enroll student in 2-5 courses
        num_courses = random.randint(2, 5)
        selected_courses = random.sample(courses, min(num_courses, len(courses)))

        for course in selected_courses:
            # Check if enrollment already exists
            query = select(CourseEnrollment).where(
                CourseEnrollment.student_id == student.id,
                CourseEnrollment.course_id == course.id,
            )
            existing = (await db.execute(query)).scalars().first()

            if existing:
                continue

            enrollment = CourseEnrollment(
                student_id=student.id,
                course_id=course.id,
            )
            db.add(enrollment)
            enrollments.append(enrollment)

    print(f"Seeded {len(enrollments)} course enrollments")
    return enrollments
