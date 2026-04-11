#!/usr/bin/env python3
"""
Database Seeder Script for Hello World Project

This script completely populates the database with test data based on the
database schemas from the backend application.

Usage:
    python seed_database.py [--env PATH] [--reset]

Options:
    --env PATH    Path to the .env file (default: apps/backend/.env)
    --reset       Drop all tables before seeding (DANGER: destroys existing data)
"""

import asyncio
import sys
import os
import argparse
from datetime import datetime, timedelta, date
from pathlib import Path
import random
import uuid

# Add the backend src directory to the Python path
BACKEND_DIR = Path(__file__).parent.parent / "apps" / "backend" / "src"
sys.path.insert(0, str(BACKEND_DIR))

# Add the backend root directory to enable src.* imports
BACKEND_ROOT = Path(__file__).parent.parent / "apps" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Import domain models and database session
from src.shared.infrastructure.session import SessionLocal, engine
from src.shared.infrastructure.base import Base
from src.shared.domain.enums import GameStatus
from sqlalchemy import select, text

# Import all domain models to register them with Base.metadata
from src.users.domain import User, Professor, Student, TeacherSettings, Role, LMSCredential
from src.game.domain import Game, GameInstance, SegmentLevel, Level
from src.statistic.domain import Feedback, MetricType, Progress, XAPIStatement
from src.sync.domain import SyncSession, SyncEvent
from src.course.domain import Course, CourseEnrollment, CourseProfessor
from src.notification.domain import Notification


class DatabaseSeeder:
    """Standalone database seeder for the Hello World Project."""

    def __init__(self, reset_db: bool = False):
        self.reset_db = reset_db
        self.db = SessionLocal()

    async def run(self):
        """Execute the complete seeding process."""
        try:
            print("=" * 70)
            print("Hello World Project - Database Seeder")
            print("=" * 70)

            # Step 0: Reset database if requested
            if self.reset_db:
                await self._reset_database()

            # Phase 1: Core data (roles and admin)
            print("\n[Phase 1] Seeding roles and admin...")
            await self._seed_roles()
            await self._seed_admin()

            # Phase 2: Users (professors and students)
            print("\n[Phase 2] Seeding users...")
            professors, students = await self._seed_all_users()

            # Phase 3: LMS credentials
            print("\n[Phase 3] Seeding LMS credentials...")
            await self._seed_lms_credentials(professors, students)

            # Phase 4: Games with levels and segments
            print("\n[Phase 4] Seeding games...")
            games = await self._seed_games()

            # Phase 5: Game instances
            print("\n[Phase 5] Seeding game instances...")
            await self._seed_game_instances(students, games)

            # Phase 6: Courses
            print("\n[Phase 6] Seeding courses...")
            courses = await self._seed_courses(professors)

            # Phase 7: Course enrollments
            print("\n[Phase 7] Seeding course enrollments...")
            await self._seed_enrollments(students, courses)

            # Phase 8: Statistics (metric types, feedbacks, progress, xAPI)
            print("\n[Phase 8] Seeding statistics...")
            await self._seed_metric_types()
            await self._seed_feedbacks(students, professors, games)
            await self._seed_progress(students)
            await self._seed_xapi_statements(students, games)

            # Phase 9: Notifications
            print("\n[Phase 9] Seeding notifications...")
            await self._seed_notifications()

            # Commit all changes
            await self.db.commit()

            print("\n" + "=" * 70)
            print("Seeding completed successfully!")
            print("=" * 70)

        except Exception as e:
            await self.db.rollback()
            print(f"\n❌ Seeding failed: {e}")
            import traceback
            traceback.print_exc()
            raise
        finally:
            await self.db.close()

    async def _reset_database(self):
        """Drop and recreate all tables. DANGER: This destroys all existing data."""
        print("\n⚠️  DANGER: Resetting database...")
        print("All existing data will be destroyed!")
        
        async with engine.begin() as conn:
            # Use CASCADE to handle foreign key dependencies
            # Execute each DROP TABLE separately (asyncpg doesn't allow multiple commands)
            tables = [
                "notifications", "sync_events", "sync_sessions",
                "course_enrollments", "course_professors", "xapi_statements",
                "progresses", "feedbacks", "game_instances", "teacher_settings",
                "students", "professors", "segment_levels", "levels", "games",
                "lms_credentials", "users", "roles", "metric_types", "courses"
            ]
            
            for table in tables:
                await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
            
            await conn.run_sync(Base.metadata.create_all)
        
        print("✓ Database reset completed")

    # ========================================================================
    # Phase 1: Core Data
    # ========================================================================

    async def _seed_roles(self):
        """Seed roles: admin, professor, student."""
        from src.users.domain.role import Role
        from sqlalchemy import select

        roles_data = [
            {"role_name": "admin", "description": "Administrator with full access"},
            {"role_name": "professor", "description": "Professor with access to teaching resources"},
            {"role_name": "student", "description": "Student with access to learning materials"},
        ]

        for role_data in roles_data:
            query = select(Role).where(Role.role_name == role_data["role_name"])
            existing = (await self.db.execute(query)).scalars().first()

            if existing:
                print(f"  ✓ Role '{role_data['role_name']}' already exists")
                continue

            role = Role(**role_data)
            self.db.add(role)
            print(f"  ✓ Seeded role: {role_data['role_name']}")

    async def _seed_admin(self):
        """Seed the admin user."""
        from src.users.domain.user import User
        from src.users.domain.role import Role
        from sqlalchemy import select

        query = select(User).where(User.username == "superadmin")
        existing = (await self.db.execute(query)).scalars().first()

        if existing:
            print("  ✓ Admin user 'superadmin' already exists")
            return

        role_query = select(Role).where(Role.role_name == "admin")
        admin_role = (await self.db.execute(role_query)).scalars().first()

        if not admin_role:
            print("  ⚠ Admin role not found. Skipping admin seeding.")
            return

        admin = User(
            username="superadmin",
            name="Admin",
            lastname="User",
            email="admin@example.com",
            is_active=True,
            hashed_password="$2b$12$h8b3DBzDYqlsA/HBVexAuukd0.KEEYYp3pvRTVOJ4pRhymA5xM73O",
            role_id=admin_role.id,
        )
        self.db.add(admin)
        print("  ✓ Seeded admin user: superadmin")

    # ========================================================================
    # Phase 2: Users
    # ========================================================================

    async def _seed_all_users(self):
        """Seed professors and students."""
        professors = await self._seed_professors()
        students = await self._seed_students()
        print(f"  ✓ Total: {len(professors)} professors, {len(students)} students")
        return professors, students

    async def _seed_professors(self):
        """Seed professor users with their profiles."""
        from src.users.domain.user import User
        from src.users.domain.professor import Professor
        from src.users.domain.teacher_settings import TeacherSettings
        from src.users.domain.role import Role
        from sqlalchemy import select

        role_query = select(Role).where(Role.role_name == "professor")
        professor_role = (await self.db.execute(role_query)).scalars().first()

        if not professor_role:
            print("  ⚠ Professor role not found")
            return []

        professors_data = [
            {
                "username": "prof_juan_perez",
                "name": "Juan",
                "lastname": "Pérez",
                "email": "juan.perez@university.edu",
                "department": "Computer Science",
                "contact_phone": "+52 555 123 4567",
            },
            {
                "username": "prof_maria_lopez",
                "name": "María",
                "lastname": "López",
                "email": "maria.lopez@university.edu",
                "department": "Mathematics",
                "contact_phone": "+52 555 234 5678",
            },
            {
                "username": "prof_carlos_garcia",
                "name": "Carlos",
                "lastname": "García",
                "email": "carlos.garcia@university.edu",
                "department": "Physics",
                "contact_phone": "+52 555 345 6789",
            },
            {
                "username": "prof_ana_martinez",
                "name": "Ana",
                "lastname": "Martínez",
                "email": "ana.martinez@university.edu",
                "department": "Chemistry",
                "contact_phone": "+52 555 456 7890",
            },
            {
                "username": "prof_roberto_sanchez",
                "name": "Roberto",
                "lastname": "Sánchez",
                "email": "roberto.sanchez@university.edu",
                "department": "Biology",
                "contact_phone": "+52 555 567 8901",
            },
        ]

        professors = []
        for data in professors_data:
            query = select(User).where(User.username == data["username"])
            existing = (await self.db.execute(query)).scalars().first()

            if existing:
                print(f"  ✓ Professor '{data['username']}' already exists")
                prof_query = select(Professor).where(Professor.user_id == existing.id)
                prof = (await self.db.execute(prof_query)).scalars().first()
                if prof:
                    professors.append(existing)
                continue

            user = User(
                username=data["username"],
                name=data["name"],
                lastname=data["lastname"],
                email=data["email"],
                hashed_password="$2b$12$SWoTdnJxZ6z.hm2tq4zEKe.OMCF1ioi1GQofQO1BUr.YUcZSpiLjO",
                is_active=True,
                role_id=professor_role.id,
            )
            self.db.add(user)
            await self.db.flush()

            professor = Professor(
                user_id=user.id,
                department=data["department"],
                contact_phone=data["contact_phone"],
            )
            self.db.add(professor)

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
            self.db.add(teacher_settings)

            professors.append(user)
            print(f"  ✓ Seeded professor: {data['username']}")

        return professors

    async def _seed_students(self):
        """Seed student users with their profiles."""
        from src.users.domain.user import User
        from src.users.domain.student import Student
        from src.users.domain.role import Role
        from sqlalchemy import select

        role_query = select(Role).where(Role.role_name == "student")
        student_role = (await self.db.execute(role_query)).scalars().first()

        if not student_role:
            print("  ⚠ Student role not found")
            return []

        students_data = [
            {"username": f"student_{i:03d}", "name": self._get_student_name(i),
             "lastname": self._get_student_lastname(i),
             "email": f"student_{i:03d}@student.edu"}
            for i in range(1, 21)
        ]

        students = []
        for data in students_data:
            query = select(User).where(User.username == data["username"])
            existing = (await self.db.execute(query)).scalars().first()

            if existing:
                print(f"  ✓ Student '{data['username']}' already exists")
                student_query = select(Student).where(Student.user_id == existing.id)
                student = (await self.db.execute(student_query)).scalars().first()
                if student:
                    students.append(existing)
                continue

            user = User(
                username=data["username"],
                name=data["name"],
                lastname=data["lastname"],
                email=data["email"],
                hashed_password="$2b$12$SWoTdnJxZ6z.hm2tq4zEKe.OMCF1ioi1GQofQO1BUr.YUcZSpiLjO",
                is_active=True,
                role_id=student_role.id,
            )
            self.db.add(user)
            await self.db.flush()

            student = Student(user_id=user.id)
            self.db.add(student)

            students.append(user)
            print(f"  ✓ Seeded student: {data['username']}")

        return students

    def _get_student_name(self, index: int) -> str:
        """Get student name by index."""
        names = [
            "Pedro", "Laura", "Miguel", "Sofia", "Diego",
            "Carmen", "Javier", "Isabella", "Luis", "Valentina",
            "Eduardo", "Natalia", "Fernando", "Andrea", "Alejandro",
            "Daniela", "Ricardo", "Gabriela", "Oscar", "Paula",
        ]
        return names[index - 1] if index <= len(names) else "Estudiante"

    def _get_student_lastname(self, index: int) -> str:
        """Get student last name by index."""
        lastnames = [
            "Álvarez", "Rodríguez", "Hernández", "Gómez", "Fernández",
            "Torres", "Reyes", "Flores", "Rivera", "Morales",
            "Castillo", "Jiménez", "Ortiz", "Vargas", "Medina",
            "Cruz", "Luna", "Ramos", "Vega", "Mendoza",
        ]
        return lastnames[index - 1] if index <= len(lastnames) else "Apellido"

    # ========================================================================
    # Phase 3: LMS Credentials
    # ========================================================================

    async def _seed_lms_credentials(self, professors, students):
        """Seed LMS credentials for professors and some students."""
        from src.users.domain.lms_credential import LMSCredential
        from sqlalchemy import select

        if not professors:
            print("  ⚠ No professors found for LMS credentials")
            return

        credentials_data = []

        # Add professors
        for prof in professors[:5]:
            credentials_data.append({
                "user": prof,
                "lms_email": prof.email,
            })

        # Add first 10 students
        for student in students[:10]:
            credentials_data.append({
                "user": student,
                "lms_email": f"lms.{student.email}",
            })

        for data in credentials_data:
            query = select(LMSCredential).where(
                LMSCredential.lms_email == data["lms_email"]
            )
            existing = (await self.db.execute(query)).scalars().first()

            if existing:
                if not data["user"].lms_id:
                    data["user"].lms_id = existing.id
                print(f"  ✓ LMS credential exists for: {data['lms_email']}")
                continue

            lms = LMSCredential(
                lms_email=data["lms_email"],
                lms_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY6fQ3Z3mK",
                lms_provider="moodle",
                lms_url="https://moodle.university.edu",
            )
            self.db.add(lms)
            await self.db.flush()

            data["user"].lms_id = lms.id
            print(f"  ✓ Seeded LMS credential for: {data['lms_email']}")

    # ========================================================================
    # Phase 4: Games
    # ========================================================================

    async def _seed_games(self):
        """Seed games with levels and segments."""
        from src.game.domain.game import Game
        from src.game.domain.level import Level
        from src.game.domain.segment_level import SegmentLevel
        from sqlalchemy import select

        games_data = [
            {
                "title": "Matemáticas Básicas",
                "description": "Aprende operaciones básicas de matemáticas de forma interactiva",
                "creator": "Dr. Juan Pérez",
                "subject": "Mathematics",
                "publication_status": "published",
                "levels": [
                    {
                        "level_number": 1,
                        "title": "Suma y Resta",
                        "description": "Operaciones básicas de suma y resta",
                        "goal": "Completar 10 operaciones correctamente",
                        "segments": [
                            {"configuration": {"type": "addition", "range": [1, 10], "count": 5}},
                            {"configuration": {"type": "subtraction", "range": [1, 10], "count": 5}},
                        ],
                    },
                    {
                        "level_number": 2,
                        "title": "Multiplicación",
                        "description": "Aprende las tablas de multiplicar",
                        "goal": "Completar tabla del 1 al 5",
                        "segments": [
                            {"configuration": {"type": "multiplication", "table": 1, "count": 10}},
                            {"configuration": {"type": "multiplication", "table": 2, "count": 10}},
                            {"configuration": {"type": "multiplication", "table": 3, "count": 10}},
                        ],
                    },
                    {
                        "level_number": 3,
                        "title": "División",
                        "description": "Operaciones de división básicas",
                        "goal": "Completar 10 divisiones correctamente",
                        "segments": [
                            {"configuration": {"type": "division", "divisor_range": [1, 5], "count": 10}},
                        ],
                    },
                ],
            },
            {
                "title": "Química Introductoria",
                "description": "Introducción a la tabla periódica y reacciones químicas",
                "creator": "Dra. María López",
                "subject": "Chemistry",
                "publication_status": "published",
                "levels": [
                    {
                        "level_number": 1,
                        "title": "Elementos Químicos",
                        "description": "Identifica los primeros 20 elementos",
                        "goal": "Reconocer 20 elementos de la tabla periódica",
                        "segments": [
                            {"configuration": {"type": "element_matching", "elements": list(range(1, 11))}},
                            {"configuration": {"type": "element_matching", "elements": list(range(11, 21))}},
                        ],
                    },
                    {
                        "level_number": 2,
                        "title": "Enlace Químico",
                        "description": "Aprende sobre tipos de enlaces",
                        "goal": "Identificar tipos de enlaces",
                        "segments": [
                            {"configuration": {"type": "bonding", "bond_types": ["ionic", "covalent", "metallic"]}},
                        ],
                    },
                ],
            },
            {
                "title": "Física Fundamental",
                "description": "Conceptos básicos de física: movimiento y fuerzas",
                "creator": "Ing. Carlos García",
                "subject": "Physics",
                "publication_status": "published",
                "levels": [
                    {
                        "level_number": 1,
                        "title": "Velocidad y Aceleración",
                        "description": "Introducción al movimiento",
                        "goal": "Calcular velocidad y aceleración",
                        "segments": [
                            {"configuration": {"type": "velocity_calc", "difficulty": "basic"}},
                            {"configuration": {"type": "acceleration_calc", "difficulty": "basic"}},
                        ],
                    },
                    {
                        "level_number": 2,
                        "title": "Leyes de Newton",
                        "description": "Las tres leyes del movimiento",
                        "goal": "Aplicar las leyes de Newton",
                        "segments": [
                            {"configuration": {"type": "newton_first", "scenarios": 5}},
                            {"configuration": {"type": "newton_second", "scenarios": 5}},
                            {"configuration": {"type": "newton_third", "scenarios": 5}},
                        ],
                    },
                ],
            },
            {
                "title": "Biología Celular",
                "description": "Estructura y función de la célula",
                "creator": "Mtro. Roberto Sánchez",
                "subject": "Biology",
                "publication_status": "published",
                "levels": [
                    {
                        "level_number": 1,
                        "title": "Partes de la Célula",
                        "description": "Identifica los organelos celulares",
                        "goal": "Reconocer 15 organelos celulares",
                        "segments": [
                            {"configuration": {
                                "type": "organelle_identification",
                                "organelles": ["nucleus", "mitochondria", "ribosome", "golgi", "er"],
                            }},
                        ],
                    },
                    {
                        "level_number": 2,
                        "title": "Procesos Celulares",
                        "description": "Mitosis y meiosis",
                        "goal": "Entender los procesos de división celular",
                        "segments": [
                            {"configuration": {
                                "type": "mitosis",
                                "stages": ["profase", "metafase", "anafase", "telofase"],
                            }},
                        ],
                    },
                ],
            },
            {
                "title": "Programación con Python",
                "description": "Aprende a programar desde cero",
                "creator": "Lic. Ana Martínez",
                "subject": "Computer Science",
                "publication_status": "published",
                "levels": [
                    {
                        "level_number": 1,
                        "title": "Variables y Tipos de Datos",
                        "description": "Introducción a Python",
                        "goal": "Crear variables y usar tipos de datos",
                        "segments": [
                            {"configuration": {"type": "variable_creation", "count": 10}},
                            {"configuration": {"type": "data_types", "types": ["int", "float", "str", "bool"]}},
                        ],
                    },
                    {
                        "level_number": 2,
                        "title": "Condicionales",
                        "description": "Sentencias if-else",
                        "goal": "Usar estructuras condicionales",
                        "segments": [
                            {"configuration": {"type": "if_statement", "exercises": 5}},
                            {"configuration": {"type": "if_else", "exercises": 5}},
                            {"configuration": {"type": "elif", "exercises": 5}},
                        ],
                    },
                    {
                        "level_number": 3,
                        "title": "Bucles",
                        "description": "Ciclos for y while",
                        "goal": "Implementar bucles correctamente",
                        "segments": [
                            {"configuration": {"type": "for_loop", "range": [1, 10]}},
                            {"configuration": {"type": "while_loop", "exercises": 5}},
                        ],
                    },
                ],
            },
        ]

        games = []
        for game_data in games_data:
            query = select(Game).where(Game.title == game_data["title"])
            existing = (await self.db.execute(query)).scalars().first()

            if existing:
                print(f"  ✓ Game '{game_data['title']}' already exists")
                games.append(existing)
                continue

            game = Game(
                title=game_data["title"],
                description=game_data["description"],
                creator=game_data["creator"],
                subject=game_data["subject"],
                publication_status=game_data["publication_status"],
            )
            self.db.add(game)
            await self.db.flush()

            for level_data in game_data.get("levels", []):
                level = Level(
                    level_number=level_data["level_number"],
                    title=level_data["title"],
                    description=level_data["description"],
                    goal=level_data["goal"],
                    game_id=game.id,
                )
                self.db.add(level)
                await self.db.flush()

                for segment_data in level_data.get("segments", []):
                    segment = SegmentLevel(
                        level_number_id=level.id,
                        configuration=segment_data["configuration"],
                    )
                    self.db.add(segment)

            games.append(game)
            print(f"  ✓ Seeded game: {game_data['title']}")

        return games

    # ========================================================================
    # Phase 5: Game Instances
    # ========================================================================

    async def _seed_game_instances(self, students, games):
        """Seed game instances for students."""
        from src.game.domain.game_instance import GameInstance
        from src.users.domain.student import Student
        from sqlalchemy import select

        if not students or not games:
            print("  ⚠ No students or games found for game instances")
            return

        students_query = select(Student).limit(10)
        students_profiles = (await self.db.execute(students_query)).scalars().all()

        instances = []
        for student in students_profiles:
            for game in games[:3]:
                for _ in range(random.randint(1, 3)):
                    started_at = datetime.now() - timedelta(days=random.randint(1, 30))
                    status = random.choice([GameStatus.COMPLETED, GameStatus.ACTIVE, GameStatus.FAILED])
                    ended_at = (
                        started_at + timedelta(minutes=random.randint(10, 60))
                        if status == GameStatus.COMPLETED
                        else None
                    )

                    instance = GameInstance(
                        started_at=started_at,
                        ended_at=ended_at,
                        status=status,
                        student_id=student.id,
                        game_id=game.id,
                    )
                    self.db.add(instance)
                    instances.append(instance)

        print(f"  ✓ Seeded {len(instances)} game instances")

    # ========================================================================
    # Phase 6: Courses
    # ========================================================================

    async def _seed_courses(self, professors):
        """Seed courses with professors."""
        from src.course.domain.course import Course
        from src.course.domain.course_professor import CourseProfessor
        from src.users.domain.professor import Professor
        from sqlalchemy import select

        professors_query = select(Professor).limit(5)
        professors_profiles = (await self.db.execute(professors_query)).scalars().all()

        if not professors_profiles:
            print("  ⚠ No professors found for courses")
            return []

        courses_data = [
            {
                "name": "Introducción a la Programación",
                "description": "Curso fundamental de programación usando Python",
                "school_year": "2024-2025",
                "period_label": "Q1",
                "display_period": "Enero - Junio 2025",
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
                "display_period": "Enero - Junio 2025",
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
                "display_period": "Enero - Junio 2025",
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
                "display_period": "Enero - Junio 2025",
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
                "display_period": "Enero - Junio 2025",
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
                "display_period": "Julio - Diciembre 2025",
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
                "display_period": "Julio - Diciembre 2025",
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
                "display_period": "Julio - Diciembre 2025",
                "start_date": "2025-07-15",
                "end_date": "2025-12-30",
                "is_active": True,
                "professor_indexes": [0],
            },
        ]

        courses = []
        for course_data in courses_data:
            query = select(Course).where(Course.name == course_data["name"])
            existing = (await self.db.execute(query)).scalars().first()

            if existing:
                print(f"  ✓ Course '{course_data['name']}' already exists")
                courses.append(existing)
                continue

            course = Course(
                name=course_data["name"],
                description=course_data["description"],
                school_year=course_data["school_year"],
                period_label=course_data["period_label"],
                display_period=course_data["display_period"],
                start_date=date.fromisoformat(course_data["start_date"]),
                end_date=date.fromisoformat(course_data["end_date"]),
                is_active=course_data["is_active"],
            )
            self.db.add(course)
            await self.db.flush()

            for prof_idx in course_data["professor_indexes"]:
                if prof_idx < len(professors_profiles):
                    course_prof = CourseProfessor(
                        course_id=course.id,
                        professor_id=professors_profiles[prof_idx].id,
                    )
                    self.db.add(course_prof)

            courses.append(course)
            print(f"  ✓ Seeded course: {course_data['name']}")

        return courses

    # ========================================================================
    # Phase 7: Course Enrollments
    # ========================================================================

    async def _seed_enrollments(self, students, courses):
        """Seed course enrollments for students."""
        from src.course.domain.course_enrollment import CourseEnrollment
        from src.users.domain.student import Student
        from src.course.domain.course import Course
        from sqlalchemy import select

        students_query = select(Student).limit(20)
        students_profiles = (await self.db.execute(students_query)).scalars().all()

        courses_query = select(Course).limit(8)
        all_courses = (await self.db.execute(courses_query)).scalars().all()

        if not students_profiles or not all_courses:
            print("  ⚠ No students or courses found for enrollments")
            return

        enrollments = []
        for student in students_profiles:
            num_courses = random.randint(2, 5)
            selected_courses = random.sample(all_courses, min(num_courses, len(all_courses)))

            for course in selected_courses:
                query = select(CourseEnrollment).where(
                    CourseEnrollment.student_id == student.id,
                    CourseEnrollment.course_id == course.id,
                )
                existing = (await self.db.execute(query)).scalars().first()

                if existing:
                    continue

                enrollment = CourseEnrollment(
                    student_id=student.id,
                    course_id=course.id,
                )
                self.db.add(enrollment)
                enrollments.append(enrollment)

        print(f"  ✓ Seeded {len(enrollments)} course enrollments")

    # ========================================================================
    # Phase 8: Statistics
    # ========================================================================

    async def _seed_metric_types(self):
        """Seed metric types."""
        from src.statistic.domain.metric_type import MetricType
        from sqlalchemy import select

        metric_types_data = [
            {"name": "Accuracy", "code": "accuracy", "description": "Percentage of correct answers"},
            {"name": "Time Spent", "code": "time_spent", "description": "Total time spent on task"},
            {"name": "Attempts", "code": "attempts", "description": "Number of attempts to complete"},
            {"name": "Hints Used", "code": "hints_used", "description": "Number of hints used"},
            {"name": "Error Rate", "code": "error_rate", "description": "Percentage of errors made"},
            {"name": "Completion Rate", "code": "completion_rate", "description": "Task completion percentage"},
            {"name": "Engagement Score", "code": "engagement", "description": "Overall engagement level"},
        ]

        for data in metric_types_data:
            query = select(MetricType).where(MetricType.code == data["code"])
            existing = (await self.db.execute(query)).scalars().first()

            if existing:
                print(f"  ✓ Metric type '{data['code']}' already exists")
                continue

            metric_type = MetricType(**data)
            self.db.add(metric_type)
            print(f"  ✓ Seeded metric type: {data['code']}")

    async def _seed_feedbacks(self, students, professors, games):
        """Seed feedbacks from students to professors."""
        from src.statistic.domain.feedback import Feedback
        from src.game.domain.level import Level
        from src.users.domain.student import Student
        from src.users.domain.professor import Professor
        from sqlalchemy import select

        students_query = select(Student).limit(10)
        students_profiles = (await self.db.execute(students_query)).scalars().all()

        professors_query = select(Professor).limit(5)
        professors_profiles = (await self.db.execute(professors_query)).scalars().all()

        games_query = select(Game).limit(3)
        all_games = (await self.db.execute(games_query)).scalars().all()

        levels_query = select(Level).limit(10)
        levels = (await self.db.execute(levels_query)).scalars().all()

        if not students_profiles or not professors_profiles:
            print("  ⚠ No students or professors found for feedbacks")
            return

        comments = [
            "Excelente metodología de enseñanza, muy clara la explicación.",
            "El contenido es muy completo, me ayudó a entender mejor el tema.",
            "Buena interacción en clase, los ejercicios son muy prácticos.",
            "El material de apoyo es muy útil para el estudio.",
            "Gracias por la paciencia y las explicaciones detalladas.",
            "Los ejemplos son muy claros y facilitan el aprendizaje.",
            "Muy buen ritmo de clase, se entiende todo perfectamente.",
            "Las evaluaciones son justas y bien estructuradas.",
            "El profesor es muy accesible para resolver dudas.",
            "Excelente curso, lo recomiendo a todos mis compañeros.",
        ]

        feedbacks = []
        for _ in range(15):
            student = random.choice(students_profiles)
            professor = random.choice(professors_profiles)
            has_game = random.choice([True, True, False])
            game = random.choice(all_games) if has_game and all_games else None
            level = random.choice(levels) if game and levels else None

            feedback = Feedback(
                comments=random.choice(comments),
                rating=random.randint(3, 5),
                student_id=student.id,
                professor_id=professor.id,
                game_id=game.id if game else None,
                level_id=level.id if level else None,
            )
            self.db.add(feedback)
            feedbacks.append(feedback)

        print(f"  ✓ Seeded {len(feedbacks)} feedbacks")

    async def _seed_progress(self, students):
        """Seed progress records for students in segments."""
        from src.statistic.domain.progress import Progress
        from src.game.domain.segment_level import SegmentLevel
        from src.users.domain.student import Student
        from sqlalchemy import select

        students_query = select(Student).limit(15)
        students_profiles = (await self.db.execute(students_query)).scalars().all()

        segments_query = select(SegmentLevel).limit(20)
        segments = (await self.db.execute(segments_query)).scalars().all()

        if not students_profiles or not segments:
            print("  ⚠ No students or segments found for progress")
            return

        progresses = []
        for student in students_profiles:
            num_segments = random.randint(3, 8)
            selected_segments = random.sample(segments, min(num_segments, len(segments)))

            for segment in selected_segments:
                progress = Progress(
                    attempt_count=random.randint(1, 5),
                    error_count=random.randint(0, 3),
                    hints_used_count=random.randint(0, 2),
                    errors_details={"errors": []},
                    objectives_completed=random.randint(0, 5),
                    efficiency_rating=random.randint(60, 100),
                    student_id=student.id,
                    segment_level_id=segment.id,
                )
                self.db.add(progress)
                progresses.append(progress)

        print(f"  ✓ Seeded {len(progresses)} progress records")

    async def _seed_xapi_statements(self, students, games):
        """Seed xAPI statements from game client."""
        from src.statistic.domain.xapi_statement import XAPIStatement
        from src.game.domain.level import Level
        from src.game.domain.segment_level import SegmentLevel
        from src.users.domain.student import Student
        from sqlalchemy import select

        students_query = select(Student).limit(10)
        students_profiles = (await self.db.execute(students_query)).scalars().all()

        games_query = select(Game).limit(3)
        all_games = (await self.db.execute(games_query)).scalars().all()

        levels_query = select(Level).limit(10)
        levels = (await self.db.execute(levels_query)).scalars().all()

        segments_query = select(SegmentLevel).limit(15)
        segments = (await self.db.execute(segments_query)).scalars().all()

        if not students_profiles or not all_games:
            print("  ⚠ No students or games found for xAPI statements")
            return

        verbs = [
            {"id": "http://adlnet.gov/expapi/verbs/initialized", "display": {"en-US": "initialized"}},
            {"id": "http://adlnet.gov/expapi/verbs/completed", "display": {"en-US": "completed"}},
            {"id": "http://adlnet.gov/expapi/verbs/passed", "display": {"en-US": "passed"}},
            {"id": "http://adlnet.gov/expapi/verbs/failed", "display": {"en-US": "failed"}},
            {"id": "http://adlnet.gov/expapi/verbs/answered", "display": {"en-US": "answered"}},
            {"id": "http://adlnet.gov/expapi/verbs/interacted", "display": {"en-US": "interacted"}},
        ]

        statements = []
        for _ in range(50):
            student = random.choice(students_profiles)
            game = random.choice(all_games)
            level = random.choice(levels) if levels else None
            segment = random.choice(segments) if segments else None
            verb = random.choice(verbs)
            timestamp = datetime.now() - timedelta(
                days=random.randint(1, 30), hours=random.randint(0, 23)
            )

            statement = XAPIStatement(
                id=str(uuid.uuid4()),
                actor_mbox=f"mailto:{student.user.email}",
                actor_account_name=student.user.username,
                actor_account_homepage="https://game.helloworld.edu",
                verb_id=verb["id"],
                verb_display=verb["display"],
                object_id=f"https://game.helloworld.edu/activities/{game.id}",
                object_type="Activity",
                object_definition_type="http://adlnet.gov/expapi/activities/game",
                object_definition_name={"en-US": game.title},
                platform="Godot Game Client",
                language="es",
                context_extensions={"extensions": {}},
                result_score_raw=str(random.randint(60, 100)),
                result_score_min="0",
                result_score_max="100",
                result_score_scaled=str(random.randint(60, 100) / 100),
                result_success=random.choice([True, True, False]),
                result_completion=random.choice([True, False]),
                result_duration=f"PT{random.randint(5, 60)}M",
                timestamp=timestamp,
                stored=timestamp,
                statement={
                    "actor": {"mbox": f"mailto:{student.user.email}"},
                    "verb": verb,
                    "object": {"id": f"https://game.helloworld.edu/activities/{game.id}"},
                    "timestamp": timestamp.isoformat(),
                },
                student_id=student.id,
                game_id=game.id,
                level_id=level.id if level else None,
                segment_id=segment.id if segment else None,
            )
            self.db.add(statement)
            statements.append(statement)

        print(f"  ✓ Seeded {len(statements)} xAPI statements")

    # ========================================================================
    # Phase 9: Notifications
    # ========================================================================

    async def _seed_notifications(self):
        """Seed notifications for users."""
        from src.notification.domain.notification import Notification
        from src.users.domain.user import User
        from sqlalchemy import select

        users_query = select(User).limit(30)
        users = (await self.db.execute(users_query)).scalars().all()

        if not users:
            print("  ⚠ No users found for notifications")
            return

        notification_templates = [
            {
                "type": "game_invite",
                "title": "Nueva invitación de juego",
                "message": "Has sido invitado a jugar 'Matemáticas Básicas'",
            },
            {
                "type": "course_enrollment",
                "title": "Matrícula confirmada",
                "message": "Tu matrícula en 'Introducción a la Programación' ha sido confirmada",
            },
            {
                "type": "feedback_received",
                "title": "Nuevo feedback recibido",
                "message": "El profesor ha enviado feedback sobre tu último juego",
            },
            {
                "type": "progress_update",
                "title": "Actualización de progreso",
                "message": "Has completado el nivel 2 de 'Física Fundamental'",
            },
            {
                "type": "achievement",
                "title": "¡Logro desbloqueado!",
                "message": "Has completado 10 juegos correctamente",
            },
            {
                "type": "system",
                "title": "Mantenimiento del sistema",
                "message": "El sistema estará en mantenimiento el domingo de 2am a 6am",
            },
            {
                "type": "reminder",
                "title": "Recordatorio de tarea",
                "message": "Tienes una tarea pendiente en 'Química Introductoria'",
            },
            {
                "type": "announcement",
                "title": "Nuevo contenido disponible",
                "message": "Se ha añadido un nuevo nivel al juego 'Programación con Python'",
            },
        ]

        notifications = []
        for user in users:
            num_notifications = random.randint(2, 5)

            for _ in range(num_notifications):
                template = random.choice(notification_templates)

                notification = Notification(
                    title=template["title"],
                    message=template["message"],
                    is_read=random.choice([True, False, False]),
                    notification_type=template["type"],
                    user_id=user.id,
                    entity_type=random.choice(["game", "course", "level", None]),
                    entity_id=None,
                )
                self.db.add(notification)
                notifications.append(notification)

        print(f"  ✓ Seeded {len(notifications)} notifications")


async def main():
    """Main entry point for the seeder script."""
    parser = argparse.ArgumentParser(description="Database Seeder for Hello World Project")
    parser.add_argument(
        "--env",
        type=str,
        default=None,
        help="Path to .env file (default: apps/backend/.env)",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset database before seeding (DANGER: destroys all data)",
    )

    args = parser.parse_args()

    # Load environment variables from .env file
    env_path = args.env or str(BACKEND_DIR.parent / ".env")
    env_file = Path(env_path)

    if env_file.exists():
        print(f"Loading environment from: {env_file}")
        from dotenv import load_dotenv
        load_dotenv(env_file)
    else:
        print(f"⚠ Warning: .env file not found at {env_file}")
        print("Using environment variables from system")

    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("\n❌ Error: DATABASE_URL environment variable is not set")
        print("\nPlease set it in your .env file or export it:")
        print("  export DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db")
        print("  export DATABASE_URL=sqlite+aiosqlite:///./test.db")
        sys.exit(1)

    print(f"Database URL: {database_url}")
    print(f"Reset database: {'Yes ⚠️' if args.reset else 'No'}")

    # Run the seeder
    seeder = DatabaseSeeder(reset_db=args.reset)
    await seeder.run()


if __name__ == "__main__":
    asyncio.run(main())
