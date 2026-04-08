from src.users.domain.user import User
from src.users.domain.professor import Professor
from src.users.domain.student import Student
from src.users.domain.teacher_settings import TeacherSettings
from src.shared.infrastructure.session import AsyncSession
from sqlalchemy import select
import uuid


async def seed_professors(db: AsyncSession):
    """Seed professor users with their profiles."""
    from src.users.domain.role import Role

    # Buscar rol de professor
    role_query = select(Role).where(Role.role_name == "professor")
    professor_role = (await db.execute(role_query)).scalars().first()

    if not professor_role:
        print("Warning: Professor role not found")
        return []

    professors_data = [
        {
            "username": "prof_juan_perez",
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez@university.edu",
            "password": "password123",
            "department": "Computer Science",
            "contact_phone": "+52 555 123 4567",
        },
        {
            "username": "prof_maria_lopez",
            "name": "María",
            "lastname": "López",
            "email": "maria.lopez@university.edu",
            "password": "password123",
            "department": "Mathematics",
            "contact_phone": "+52 555 234 5678",
        },
        {
            "username": "prof_carlos_garcia",
            "name": "Carlos",
            "lastname": "García",
            "email": "carlos.garcia@university.edu",
            "password": "password123",
            "department": "Physics",
            "contact_phone": "+52 555 345 6789",
        },
        {
            "username": "prof_ana_martinez",
            "name": "Ana",
            "lastname": "Martínez",
            "email": "ana.martinez@university.edu",
            "password": "password123",
            "department": "Chemistry",
            "contact_phone": "+52 555 456 7890",
        },
        {
            "username": "prof_roberto_sanchez",
            "name": "Roberto",
            "lastname": "Sánchez",
            "email": "roberto.sanchez@university.edu",
            "password": "password123",
            "department": "Biology",
            "contact_phone": "+52 555 567 8901",
        },
    ]

    professors = []
    for data in professors_data:
        # Check if user exists
        query = select(User).where(User.username == data["username"])
        existing = (await db.execute(query)).scalars().first()

        if existing:
            print(f"Professor user '{data['username']}' already exists")
            # Get the professor profile
            prof_query = select(Professor).where(Professor.user_id == existing.id)
            prof = (await db.execute(prof_query)).scalars().first()
            if prof:
                professors.append(existing)
            continue

        # Create user
        user = User(
            username=data["username"],
            name=data["name"],
            lastname=data["lastname"],
            email=data["email"],
            hashed_password="$2b$12$SWoTdnJxZ6z.hm2tq4zEKe.OMCF1ioi1GQofQO1BUr.YUcZSpiLjO",  # password123
            is_active=True,
            role_id=professor_role.id,
        )
        db.add(user)
        await db.flush()

        # Create professor profile
        professor = Professor(
            user_id=user.id,
            department=data["department"],
            contact_phone=data["contact_phone"],
        )
        db.add(professor)

        # Create teacher settings
        teacher_settings = TeacherSettings(
            user_id=user.id,
            theme="light",
            notifications_enabled=True,
            notification_frequency="realtime",
            interface_language="es",
            auto_logout=False,
            session_duration_minutes=60,
            remember_login=True,
            color_theme="blue",
            animations_enabled=True,
            email_notifications=True,
            date_format="DD/MM/YYYY",
            timezone="America/Mexico_City",
        )
        db.add(teacher_settings)

        professors.append(user)
        print(f"Seeded professor: {data['username']}")

    return professors


async def seed_students(db: AsyncSession):
    """Seed student users with their profiles."""
    from src.users.domain.role import Role

    # Buscar rol de student
    role_query = select(Role).where(Role.role_name == "student")
    student_role = (await db.execute(role_query)).scalars().first()

    if not student_role:
        print("Warning: Student role not found")
        return []

    students_data = [
        {
            "username": "student_001",
            "name": "Pedro",
            "lastname": "Álvarez",
            "email": "pedro.alvarez@student.edu",
        },
        {
            "username": "student_002",
            "name": "Laura",
            "lastname": "Rodríguez",
            "email": "laura.rodriguez@student.edu",
        },
        {
            "username": "student_003",
            "name": "Miguel",
            "lastname": "Hernández",
            "email": "miguel.hernandez@student.edu",
        },
        {
            "username": "student_004",
            "name": "Sofia",
            "lastname": "Gómez",
            "email": "sofia.gomez@student.edu",
        },
        {
            "username": "student_005",
            "name": "Diego",
            "lastname": "Fernández",
            "email": "diego.fernandez@student.edu",
        },
        {
            "username": "student_006",
            "name": "Carmen",
            "lastname": "Torres",
            "email": "carmen.torres@student.edu",
        },
        {
            "username": "student_007",
            "name": "Javier",
            "lastname": "Reyes",
            "email": "javier.reyes@student.edu",
        },
        {
            "username": "student_008",
            "name": "Isabella",
            "lastname": "Flores",
            "email": "isabella.flores@student.edu",
        },
        {
            "username": "student_009",
            "name": "Luis",
            "lastname": "Rivera",
            "email": "luis.rivera@student.edu",
        },
        {
            "username": "student_010",
            "name": "Valentina",
            "lastname": "Morales",
            "email": "valentina.morales@student.edu",
        },
        {
            "username": "student_011",
            "name": "Eduardo",
            "lastname": "Castillo",
            "email": "eduardo.castillo@student.edu",
        },
        {
            "username": "student_012",
            "name": "Natalia",
            "lastname": "Jiménez",
            "email": "natalia.jimenez@student.edu",
        },
        {
            "username": "student_013",
            "name": "Fernando",
            "lastname": "Ortiz",
            "email": "fernando.ortiz@student.edu",
        },
        {
            "username": "student_014",
            "name": "Andrea",
            "lastname": "Vargas",
            "email": "andrea.vargas@student.edu",
        },
        {
            "username": "student_015",
            "name": "Alejandro",
            "lastname": "Medina",
            "email": "alejandro.medina@student.edu",
        },
        {
            "username": "student_016",
            "name": "Daniela",
            "lastname": "Cruz",
            "email": "daniela.cruz@student.edu",
        },
        {
            "username": "student_017",
            "name": "Ricardo",
            "lastname": "Luna",
            "email": "ricardo.luna@student.edu",
        },
        {
            "username": "student_018",
            "name": "Gabriela",
            "lastname": "Ramos",
            "email": "gabriela.ramos@student.edu",
        },
        {
            "username": "student_019",
            "name": "Oscar",
            "lastname": "Vega",
            "email": "oscar.vega@student.edu",
        },
        {
            "username": "student_020",
            "name": "Paula",
            "lastname": "Mendoza",
            "email": "paula.mendoza@student.edu",
        },
    ]

    students = []
    for data in students_data:
        # Check if user exists
        query = select(User).where(User.username == data["username"])
        existing = (await db.execute(query)).scalars().first()

        if existing:
            print(f"Student user '{data['username']}' already exists")
            # Check if student profile exists
            student_query = select(Student).where(Student.user_id == existing.id)
            student = (await db.execute(student_query)).scalars().first()
            if student:
                students.append(existing)
            continue

        # Create user
        user = User(
            username=data["username"],
            name=data["name"],
            lastname=data["lastname"],
            email=data["email"],
            hashed_password="$2b$12$SWoTdnJxZ6z.hm2tq4zEKe.OMCF1ioi1GQofQO1BUr.YUcZSpiLjO",  # password123
            is_active=True,
            role_id=student_role.id,
        )
        db.add(user)
        await db.flush()

        # Create student profile
        student = Student(user_id=user.id)
        db.add(student)

        students.append(user)
        print(f"Seeded student: {data['username']}")

    return students


async def seed_all_users(db: AsyncSession):
    """Seed all users (professors and students)."""
    print("Seeding professors...")
    professors = await seed_professors(db)

    print("Seeding students...")
    students = await seed_students(db)

    print(f"Seeded {len(professors)} professors and {len(students)} students")
    return professors, students
