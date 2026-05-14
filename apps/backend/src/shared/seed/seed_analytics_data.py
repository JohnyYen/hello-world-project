#!/usr/bin/env python3
"""
Seed de datos de prueba para el dashboard de analytics.
VERSIÓN LIMPIA - Solo agrega datos, NO borra tablas.

Este script crea:
- Cursos de diferentes períodos escolares (2024-2025 Q1, Q2, 2025-2026 Q1)
- Estudiantes inscritos en múltiples cursos
- Sesiones de sync con eventos que generan analíticas
"""

import asyncio
import random
import uuid
from datetime import datetime, timedelta, date
from typing import List

from src.shared.infrastructure.session import SessionLocal
from src.shared.infrastructure.base import Base

# Domain models - Import ALL needed models to avoid mapper errors
from src.users.domain.user import User
from src.users.domain.role import Role
from src.users.domain.professor import Professor
from src.users.domain.student import Student
from src.users.domain.notification import Notification
from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment
from src.course.domain.course_professor import CourseProfessor
from src.game.domain.game import Game
from src.game.domain.level import Level
from src.game.domain.segment_level import SegmentLevel
from src.game.domain.game_instance import GameInstance
from src.sync.domain.sync_session import SyncSession
from src.sync.domain.sync_event import SyncEvent
from src.statistic.domain.progress import Progress
from src.statistic.domain.xapi_statement import XAPIStatement
from src.statistic.domain.feedback import Feedback

from sqlalchemy import select


# ============================================
# DATOS DE ESTUDIANTES
# ============================================
STUDENT_NAMES = [
    ("Juan", "Álvarez", "juan.alvarez@student.edu"),
    ("Laura", "Rodríguez", "laura.rodriguez@student.edu"),
    ("Miguel", "Hernández", "miguel.hernandez@student.edu"),
    ("Sofía", "Gómez", "sofia.gomez@student.edu"),
    ("Diego", "Fernández", "diego.fernandez@student.edu"),
    ("Carmen", "Torres", "carmen.torres@student.edu"),
    ("Javier", "Reyes", "javier.reyes@student.edu"),
    ("Isabella", "Flores", "isabella.flores@student.edu"),
    ("Luis", "Rivera", "luis.rivera@student.edu"),
    ("Valentina", "Morales", "valentina.morales@student.edu"),
    ("Eduardo", "Castillo", "eduardo.castillo@student.edu"),
    ("Natalia", "Jiménez", "natalia.jimenez@student.edu"),
    ("Fernando", "Ortiz", "fernando.ortiz@student.edu"),
    ("Andrea", "Vargas", "andrea.vargas@student.edu"),
    ("Alejandro", "Medina", "alejandro.medina@student.edu"),
    ("Daniela", "Cruz", "daniela.cruz@student.edu"),
    ("Ricardo", "Luna", "ricardo.luna@student.edu"),
    ("Gabriela", "Ramos", "gabriela.ramos@student.edu"),
    ("Óscar", "Vega", "oscar.vega@student.edu"),
    ("Paula", "Mendoza", "paula.mendoza@student.edu"),
    ("Marco", "Delgado", "marco.delgado@student.edu"),
    ("Ana", "Castro", "ana.castro@student.edu"),
    ("Sergio", "Muñoz", "sergio.munoz@student.edu"),
    ("Elena", "Ibáñez", "elena.ibanez@student.edu"),
    ("Roberto", "Núñez", "roberto.nunez@student.edu"),
    ("María", "Gil", "maria.gil@student.edu"),
    ("Carlos", "Ruiz", "carlos.ruiz@student.edu"),
    ("Laura", "Serrano", "laura.serrano@student.edu"),
    ("Pedro", "Ortega", "pedro.ortega@student.edu"),
    ("Rosa", "Molina", "rosa.molina@student.edu"),
    ("Alberto", "Navarro", "alberto.navarro@student.edu"),
    ("Sandra", "Pérez", "sandra.perez@student.edu"),
    ("Jorge", "Vargas", "jorge.vargas@student.edu"),
    ("Lucía", "Ramírez", "lucia.ramirez@student.edu"),
    ("Miguel", "Torres", "miguel.torres@student.edu"),
    ("Sara", "Herrera", "sara.herrera@student.edu"),
    ("David", "Cortés", "david.cortes@student.edu"),
    ("Claudia", "Medina", "claudia.medina@student.edu"),
    ("Raúl", "Flores", "raul.flores@student.edu"),
]

# ============================================
# CURSOS POR PERÍODO ESCOLAR
# ============================================
COURSES_DATA = [
    # 2024-2025 School Year
    {
        "school_year": "2024-2025",
        "periods": [
            {
                "period_label": "Q1",
                "start_date": date(2025, 1, 15),
                "end_date": date(2025, 6, 30),
                "courses": [
                    {"name": "Introducción a la Programación", "subject": "Computer Science"},
                    {"name": "Matemáticas Discretas", "subject": "Mathematics"},
                    {"name": "Química General", "subject": "Chemistry"},
                ]
            },
            {
                "period_label": "Q2",
                "start_date": date(2025, 7, 15),
                "end_date": date(2025, 12, 20),
                "courses": [
                    {"name": "Estructuras de Datos", "subject": "Computer Science"},
                    {"name": "Cálculo Diferencial", "subject": "Mathematics"},
                    {"name": "Física I", "subject": "Physics"},
                ]
            },
        ]
    },
    # 2025-2026 School Year
    {
        "school_year": "2025-2026",
        "periods": [
            {
                "period_label": "Q1",
                "start_date": date(2026, 1, 15),
                "end_date": date(2026, 6, 30),
                "courses": [
                    {"name": "Introducción a la Programación", "subject": "Computer Science"},
                    {"name": "Álgebra Lineal", "subject": "Mathematics"},
                    {"name": "Biología Celular", "subject": "Biology"},
                    {"name": "Programación Visual", "subject": "Computer Science"},
                ]
            },
        ]
    },
]

# ============================================
# TIPOS DE EVENTOS DE SYNC
# ============================================
EVENT_TYPES = [
    "game.started",
    "level.started", 
    "level.completed",
    "level.failed",
    "block.placed",
    "block.removed",
    "block.connected",
    "variable.assigned",
    "condition.executed",
    "loop.executed",
    "function.called",
    "hint.requested",
    "error.created",
    "error.corrected",
    "segment.completed",
    "game.completed",
]


async def seed_students_only(db: SessionLocal) -> List[Student]:
    """Crea estudiantes sin borrar nada existente."""
    print("\n[Students]")
    
    # Get student role
    role_query = select(Role).where(Role.role_name == "student")
    student_role = (await db.execute(role_query)).scalars().first()
    
    if not student_role:
        print("✗ Rol de estudiante no encontrado")
        return []
    
    students = []
    for first_name, lastname, email in STUDENT_NAMES:
        username = f"{first_name.lower()}.{lastname.lower()}"
        
        # Check if user exists
        user_query = select(User).where(User.email == email)
        existing = (await db.execute(user_query)).scalars().first()
        
        if existing:
            student_query = select(Student).where(Student.user_id == existing.id)
            student = (await db.execute(student_query)).scalars().first()
            if student:
                students.append(student)
            continue
        
        # Create user
        user = User(
            username=username,
            name=first_name,
            lastname=lastname,
            email=email,
            hashed_password="$2b$12$SWoTdnJxZ6z.hm2tq4zEKe.OMCF1ioi1GQofQO1BUr.YUcZSpiLjO",
            is_active=True,
            role_id=student_role.id,
        )
        db.add(user)
        await db.flush()
        
        # Create student profile
        student = Student(user_id=user.id)
        db.add(student)
        students.append(student)
    
    await db.commit()
    print(f"✓ {len(students)} estudiantes verificados/creados")
    return students


async def seed_courses_analytics(db: SessionLocal) -> List[Course]:
    """Crea cursos por período escolar sin borrar nada."""
    print("\n[Courses]")
    
    # Get professors
    prof_query = select(Professor)
    professors = (await db.execute(prof_query)).scalars().all()
    
    if not professors:
        print("✗ No hay profesores disponibles")
        return []
    
    courses = []
    
    for year_data in COURSES_DATA:
        school_year = year_data["school_year"]
        
        for period_data in year_data["periods"]:
            period_label = period_data["period_label"]
            start_date = period_data["start_date"]
            end_date = period_data["end_date"]
            
            for course_info in period_data["courses"]:
                name = course_info["name"]
                
                # Check if exists
                query = select(Course).where(
                    Course.name == name,
                    Course.school_year == school_year,
                    Course.period_label == period_label,
                )
                existing = (await db.execute(query)).scalars().first()
                
                if existing:
                    courses.append(existing)
                    continue
                
                # Create course
                course = Course(
                    name=name,
                    description=f"Curso de {course_info['subject']}",
                    school_year=school_year,
                    period_label=period_label,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True,
                )
                db.add(course)
                await db.flush()
                
                # Add professor
                prof = professors[len(courses) % len(professors)]
                course_prof = CourseProfessor(
                    course_id=course.id,
                    professor_id=prof.id,
                )
                db.add(course_prof)
                
                courses.append(course)
                print(f"  ✓ {name} ({school_year} {period_label})")
    
    await db.commit()
    print(f"✓ {len(courses)} cursos verificados/creados")
    return courses


async def seed_enrollments_analytics(db: SessionLocal, students: List[Student], courses: List[Course]):
    """Inscribe estudiantes en cursos sin duplicados."""
    print("\n[Enrollments]")
    
    # Group courses by period
    period_courses = {}
    for course in courses:
        key = f"{course.school_year}-{course.period_label}"
        if key not in period_courses:
            period_courses[key] = []
        period_courses[key].append(course)
    
    enrollments_count = 0
    
    for student in students:
        num_courses = random.randint(3, 5)
        
        all_period_keys = list(period_courses.keys())
        if not all_period_keys:
            continue
            
        selected_periods = random.sample(all_period_keys, min(num_courses, len(all_period_keys)))
        
        for period_key in selected_periods:
            period_course_list = period_courses[period_key]
            course = random.choice(period_course_list)
            
            # Check if already enrolled
            query = select(CourseEnrollment).where(
                CourseEnrollment.student_id == student.id,
                CourseEnrollment.course_id == course.id,
            )
            existing = (await db.execute(query)).scalars().first()
            
            if not existing:
                enrollment = CourseEnrollment(
                    student_id=student.id,
                    course_id=course.id,
                )
                db.add(enrollment)
                enrollments_count += 1
    
    await db.commit()
    print(f"✓ {enrollments_count} nuevas inscripciones creadas")


async def seed_games_levels_analytics(db: SessionLocal) -> tuple:
    """Crea juegos, niveles y segmentos."""
    print("\n[Games & Levels]")
    
    games_data = [
        {
            "title": "Programación Visual - Bloques",
            "description": "Aprende programación con bloques visuales",
            "subject": "Computer Science",
            "levels": [
                {"level_number": 1, "title": "Variables", "description": "Introducción a variables"},
                {"level_number": 2, "title": "Condicionales", "description": "Sentencias if-else"},
                {"level_number": 3, "title": "Bucles", "description": "Ciclos for y while"},
                {"level_number": 4, "title": "Funciones", "description": "Crear y llamar funciones"},
            ]
        },
        {
            "title": "Matemáticas Interactivas",
            "description": "Ejercicios de matemáticas",
            "subject": "Mathematics",
            "levels": [
                {"level_number": 1, "title": "Operaciones Básicas", "description": "Suma, resta, multiplicación"},
                {"level_number": 2, "title": "Álgebra", "description": "Ecuaciones simples"},
            ]
        },
    ]
    
    games = []
    all_segments = []
    
    for game_data in games_data:
        # Check if exists
        query = select(Game).where(Game.title == game_data["title"])
        existing = (await db.execute(query)).scalars().first()
        
        if existing:
            game = existing
            print(f"  ✓ Juego existente: {game_data['title']}")
        else:
            game = Game(
                title=game_data["title"],
                description=game_data["description"],
                creator="System",
                subject=game_data["subject"],
                publication_status="published",
            )
            db.add(game)
            await db.flush()
            print(f"  ✓ Juego creado: {game_data['title']}")
        
        # Create levels
        for level_data in game_data["levels"]:
            query = select(Level).where(
                Level.game_id == game.id,
                Level.level_number == level_data["level_number"],
            )
            existing = (await db.execute(query)).scalars().first()
            
            if existing:
                level = existing
            else:
                level = Level(
                    level_number=level_data["level_number"],
                    title=level_data["title"],
                    description=level_data["description"],
                    goal="Complete the level",
                    game_id=game.id,
                )
                db.add(level)
                await db.flush()
            
            # Get or create segments (2-3 per level)
            for i in range(1, random.randint(2, 4)):
                query = select(SegmentLevel).where(
                    SegmentLevel.level_number_id == level.id,
                )
                existing_seg = (await db.execute(query)).scalars().first()
                
                if not existing_seg:
                    segment = SegmentLevel(
                        level_number_id=level.id,
                        configuration={"type": f"exercise_{i}", "count": 5},
                    )
                    db.add(segment)
                    all_segments.append(segment)
                else:
                    all_segments.append(existing_seg)
        
        games.append(game)
    
    await db.commit()
    print(f"✓ {len(games)} juegos con niveles y segmentos")
    return games, all_segments


async def seed_sync_and_analytics(
    db: SessionLocal, 
    students: List[Student], 
    games: List[Game],
    segments: List[SegmentLevel],
):
    """Crea instancias de juego y sesiones de sync con eventos."""
    print("\n[Game Instances & Sync Events]")
    
    if not segments:
        print("✗ No hay segmentos disponibles")
        return
    
    # Pre-load student user data to avoid lazy loading issues
    from sqlalchemy.orm import selectinload
    students_with_users = (await db.execute(
        select(Student).options(selectinload(Student.user))
    )).scalars().all()
    
    # Create a dict for quick access
    student_dict = {s.id: s for s in students_with_users}
    
    instances_count = 0
    
    for student in students_with_users:
        num_instances = random.randint(2, 4)
        
        for _ in range(num_instances):
            game = random.choice(games)
            started_at = datetime.now() - timedelta(
                days=random.randint(1, 60),
                hours=random.randint(0, 23),
            )
            
            # Create game instance
            instance = GameInstance(
                started_at=started_at,
                ended_at=None,
                status="active",
                student_id=student.id,
                game_id=game.id,
            )
            db.add(instance)
            await db.flush()
            
            # Create sync session
            sync_session = SyncSession(
                start_time=started_at,
                end_time=None,
                status="active",
                instance_id=instance.id,
            )
            db.add(sync_session)
            await db.flush()
            
            # Create 5-15 sync events per session
            num_events = random.randint(5, 15)
            for i in range(num_events):
                event_time = started_at + timedelta(minutes=i * random.randint(1, 3))
                event_type = random.choice(EVENT_TYPES)
                
                payload = {
                    "level": random.randint(1, 3),
                    "block_id": f"block_{random.randint(100, 999)}",
                    "timestamp": event_time.isoformat(),
                }
                
                if "completed" in event_type:
                    payload["score"] = random.randint(60, 100)
                    payload["duration_seconds"] = random.randint(60, 600)
                
                if "error" in event_type:
                    payload["error_message"] = "Syntax error"
                    payload["error_line"] = random.randint(1, 20)
                
                sync_event = SyncEvent(
                    event_type=event_type,
                    payload=payload,
                    timestamp=event_time,
                    status="processed" if random.random() > 0.2 else "pending",
                    sync_session_id=sync_session.id,
                )
                db.add(sync_event)
                
                # Create progress if completed
                if "completed" in event_type or random.random() > 0.7:
                    segment = random.choice(segments)
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
                    db.add(progress)
                
                # Create xAPI statement occasionally
                if random.random() > 0.5:
                    verb = "completed" if "completed" in event_type else "interacted"
                    stmt_id = str(uuid.uuid4())
                    
                    xapi = XAPIStatement(
                        id=stmt_id,
                        actor_mbox=f"mailto:{student.user.email}",
                        actor_account_name=student.user.username,
                        actor_account_homepage="https://game.helloworld.edu",
                        verb_id=f"http://adlnet.gov/expapi/verbs/{verb}",
                        verb_display={"en-US": verb},
                        object_id=f"https://game.helloworld.edu/activities/{game.id}",
                        object_type="Activity",
                        object_definition_type="http://adlnet.gov/expapi/activities/game",
                        object_definition_name={"en-US": game.title},
                        platform="Godot Game Client",
                        language="es",
                        context_extensions={},
                        result_score_raw=str(random.randint(60, 100)),
                        result_score_min="0",
                        result_score_max="100",
                        result_score_scaled=str(random.randint(60, 100) / 100),
                        result_success="completed" in event_type,
                        result_completion="completed" in event_type,
                        result_duration=f"PT{random.randint(5, 30)}M",
                        timestamp=event_time,
                        stored=event_time,
                        statement={},
                        student_id=student.id,
                        game_id=game.id,
                    )
                    db.add(xapi)
            
            # End the session sometimes
            if random.random() > 0.3:
                sync_session.end_time = started_at + timedelta(minutes=random.randint(10, 30))
                sync_session.status = "completed"
                instance.ended_at = sync_session.end_time
                instance.status = "completed"
            
            instances_count += 1
    
    await db.commit()
    print(f"✓ {instances_count} instancias de juego con sync events creadas")


async def seed_feedbacks_analytics(db: SessionLocal, students: List[Student], professors: List[Professor]):
    """Crea feedbacks de estudiantes."""
    print("\n[Feedbacks]")
    
    comments = [
        "Excelente metodología, muy clara la explicación.",
        "El contenido es muy completo, me ayudó a entender.",
        "Buena interacción en clase, ejercicios prácticos.",
        "El material de apoyo es muy útil para estudiar.",
        "Gracias por la paciencia y explicaciones.",
        "Los ejemplos son muy claros.",
        "Muy buen ritmo de clase.",
        "Las evaluaciones son justas.",
        "El professor es muy accesible.",
        "Excelente curso, lo recomiendo.",
    ]
    
    feedbacks_count = 0
    for student in students[:20]:
        for _ in range(random.randint(1, 3)):
            professor = random.choice(professors)
            
            feedback = Feedback(
                comments=random.choice(comments),
                rating=random.randint(3, 5),
                student_id=student.id,
                professor_id=professor.id,
            )
            db.add(feedback)
            feedbacks_count += 1
    
    await db.commit()
    print(f"✓ {feedbacks_count} feedbacks creados")


async def main():
    """Ejecuta todo el seed sin borrar datos existentes."""
    print("\n" + "="*50)
    print("SEED DE DATOS PARA ANALYTICS DASHBOARD")
    print("="*50 + "\n")
    
    db = SessionLocal()
    try:
        # Seed students
        students = await seed_students_only(db)
        
        # Seed courses
        courses = await seed_courses_analytics(db)
        
        # Seed enrollments
        await seed_enrollments_analytics(db, students, courses)
        
        # Seed games/levels/segments
        games, segments = await seed_games_levels_analytics(db)
        
        # Get professors for feedback
        prof_query = select(Professor)
        professors = (await db.execute(prof_query)).scalars().all()
        
        # Seed game instances and sync events
        await seed_sync_and_analytics(db, students, games, segments)
        
        # Seed feedbacks
        await seed_feedbacks_analytics(db, students, professors)
        
        print("\n" + "="*50)
        print("SEED COMPLETADO!")
        print("="*50)
        print(f"""
Resumen:
- Estudiantes: {len(students)}
- Cursos: {len(courses)}
- Juegos: {len(games)}
- Instancias de juego con eventos y analíticas creadas
- Feedbacks generados
        """)
    except Exception as e:
        await db.rollback()
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())