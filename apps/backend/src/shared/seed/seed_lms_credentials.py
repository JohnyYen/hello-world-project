from src.users.domain.lms_credential import LMSCredential
from src.shared.infrastructure.session import AsyncSession
from sqlalchemy import select


async def seed_lms_credentials(db: AsyncSession):
    """Seed LMS credentials for users."""
    from src.users.domain.user import User
    from src.users.domain.role import Role

    # Buscar rol de professor
    professor_role_query = select(Role).where(Role.role_name == "professor")
    professor_role = (await db.execute(professor_role_query)).scalars().first()

    # Buscar rol de student
    student_role_query = select(Role).where(Role.role_name == "student")
    student_role = (await db.execute(student_role_query)).scalars().first()

    # Obtener usuarios profesores y estudiantes
    professors_query = select(User).where(User.role_id == professor_role.id).limit(5)
    professors = (await db.execute(professors_query)).scalars().all()

    students_query = select(User).where(User.role_id == student_role.id).limit(20)
    students = (await db.execute(students_query)).scalars().all()

    # Datos de LMS credentials - profesor + 10 estudiantes
    lms_credentials_data = [
        {"user": professors[0], "lms_email": "juan.perez@university.edu"},
        {"user": professors[1], "lms_email": "maria.lopez@university.edu"},
        {"user": professors[2], "lms_email": "carlos.garcia@university.edu"},
        {"user": professors[3], "lms_email": "ana.martinez@university.edu"},
        {"user": professors[4], "lms_email": "roberto.sanchez@university.edu"},
        {"user": students[0], "lms_email": "student.alumno1@student.edu"},
        {"user": students[1], "lms_email": "student.alumno2@student.edu"},
        {"user": students[2], "lms_email": "student.alumno3@student.edu"},
        {"user": students[3], "lms_email": "student.alumno4@student.edu"},
        {"user": students[4], "lms_email": "student.alumno5@student.edu"},
        {"user": students[5], "lms_email": "student.alumno6@student.edu"},
        {"user": students[6], "lms_email": "student.alumno7@student.edu"},
        {"user": students[7], "lms_email": "student.alumno8@student.edu"},
        {"user": students[8], "lms_email": "student.alumno9@student.edu"},
        {"user": students[9], "lms_email": "student.alumno10@student.edu"},
    ]

    for data in lms_credentials_data:
        # Check if LMS credential already exists
        query = select(LMSCredential).where(
            LMSCredential.lms_email == data["lms_email"]
        )
        existing = (await db.execute(query)).scalars().first()

        if existing:
            # Just update the user's lms_id if it doesn't have one
            if not data["user"].lms_id:
                data["user"].lms_id = existing.id
            print(f"LMS credential already exists for: {data['lms_email']}")
            continue

        lms = LMSCredential(
            lms_email=data["lms_email"],
            lms_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY6fQ3Z3mK",  # password123
            lms_provider="moodle",
            lms_url="https://moodle.university.edu",
        )
        db.add(lms)
        await db.flush()

        # Actualizar el usuario con el ID de credencial
        data["user"].lms_id = lms.id
        print(f"Seeded LMS credential for: {data['lms_email']}")
