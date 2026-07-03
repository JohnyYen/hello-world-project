#!/usr/bin/env python3
"""
Seed de datos realistas para pruebas de dashboard y analytics.
Genera 5 meses de datos (Febrero - Junio 2026) con patrones realistas.

USO:
    uv run python scripts/seed_realistic_data.py

NO borra datos existentes - solo agrega.
IDEMPOTENTE - se puede ejecutar múltiples veces sin duplicar.
"""

import asyncio
import random
import uuid
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional
from collections import defaultdict

# Add the backend src directory to the Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "apps" / "backend" / "src"
sys.path.insert(0, str(BACKEND_DIR))
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Load .env manually BEFORE importing settings (pydantic-settings needs it)
ENV_PATH = BACKEND_ROOT / ".env"
if ENV_PATH.exists():
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'").strip('"')
            if key == "DATABASE_URL":
                # Convert Docker hostname to localhost for local execution
                val = val.replace("@postgresql_db:", "@localhost:")
                val = val.replace("@postgres:", "@localhost:")
            if key not in os.environ:
                os.environ[key] = val

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from src.shared.infrastructure.session import SessionLocal
from src.shared.infrastructure.base import Base

# Domain models
from src.users.domain.user import User
from src.users.domain.role import Role
from src.users.domain.professor import Professor
from src.users.domain.student import Student
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

# ============================================
# CONFIGURACIÓN
# ============================================

HELLO_WORLD_TITLE = "Hello World"

# Período de 5 meses: Febrero 1 - Junio 23, 2026
DATA_START = datetime(2026, 2, 1, 8, 0, 0, tzinfo=None)
DATA_END = datetime(2026, 6, 23, 18, 0, 0, tzinfo=None)

# Game IDs (se resolverán dinámicamente)
GAME_MAPPING = {
    "Matemáticas Interactivas": {"slug": "matematicas", "subject": "Mathematics"},
    "Programación Visual - Bloques": {"slug": "programacion-visual", "subject": "Computer Science"},
}

# Asignación de juegos a cursos (por nombre de curso)
# Los cursos se matchean por nombre (case-insensitive)
COURSE_GAME_ASSIGNMENTS = [
    # Matemáticas Interactivas → cursos de matemáticas/ciencias
    ("Álgebra Lineal", "Matemáticas Interactivas"),
    ("Cálculo Diferencial", "Matemáticas Interactivas"),
    ("Matemáticas Discretas", "Matemáticas Interactivas"),
    ("Matematicas", "Matemáticas Interactivas"),
    ("Biología Celular", "Matemáticas Interactivas"),
    ("Física I", "Matemáticas Interactivas"),
    ("Química General", "Matemáticas Interactivas"),
    # Programación Visual → cursos de computación
    ("Introducción a la Programación", "Programación Visual - Bloques"),
    ("Estructuras de Datos", "Programación Visual - Bloques"),
    ("Programación Visual", "Programación Visual - Bloques"),
    ("IP", "Programación Visual - Bloques"),
    ("DPOO", "Programación Visual - Bloques"),
    ("Socialismo", "Programación Visual - Bloques"),
]

# Verbos xAPI
XAPI_VERBS = {
    "interacted": {"id": "http://adlnet.gov/expapi/verbs/interacted", "display": {"en-US": "interacted"}},
    "completed": {"id": "http://adlnet.gov/expapi/verbs/completed", "display": {"en-US": "completed"}},
    "attempted": {"id": "http://adlnet.gov/expapi/verbs/attempted", "display": {"en-US": "attempted"}},
    "progressed": {"id": "http://adlnet.gov/expapi/verbs/progressed", "display": {"en-US": "progressed"}},
    "failed": {"id": "http://adlnet.gov/expapi/verbs/failed", "display": {"en-US": "failed"}},
}

# Tipos de eventos de sync
SYNC_EVENT_TYPES = [
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

# ============================================
# PERFILES DE ESTUDIANTES (para distribución realista)
# ============================================

# Distribución: 20% alto, 50% medio, 20% bajo, 10% inactivo
STUDENT_PROFILES = ["high", "medium", "medium", "medium", "low", "low", "inactive"]
# Expand to match 7: 1 high, 3 medium, 2 low, 1 inactive
# Actually let's use weights: high=0.2, medium=0.5, low=0.2, inactive=0.1

PROFILE_WEIGHTS = [0.2, 0.5, 0.2, 0.1]
PROFILE_TYPES = ["high", "medium", "low", "inactive"]

def assign_profile() -> str:
    return random.choices(PROFILE_TYPES, weights=PROFILE_WEIGHTS, k=1)[0]


def sessions_per_week(profile: str) -> int:
    """Cuántas sesiones por semana según el perfil."""
    if profile == "high":
        return random.randint(3, 5)
    elif profile == "medium":
        return random.randint(2, 4)
    elif profile == "low":
        return random.randint(1, 2)
    else:  # inactive
        return random.randint(0, 1)


def score_range(profile: str) -> tuple:
    """Rango de puntuación según perfil (min, max)."""
    if profile == "high":
        return (80, 100)
    elif profile == "medium":
        return (55, 90)
    elif profile == "low":
        return (30, 70)
    else:
        return (20, 60)


def attempts_range(profile: str) -> tuple:
    """Intentos por nivel según perfil (min, max)."""
    if profile == "high":
        return (1, 2)
    elif profile == "medium":
        return (2, 5)
    elif profile == "low":
        return (4, 8)
    else:
        return (1, 3)


def hints_range(profile: str) -> tuple:
    if profile == "high":
        return (0, 1)
    elif profile == "medium":
        return (1, 3)
    elif profile == "low":
        return (2, 5)
    else:
        return (0, 2)


def efficiency_range(profile: str) -> tuple:
    if profile == "high":
        return (85, 100)
    elif profile == "medium":
        return (60, 90)
    elif profile == "low":
        return (35, 65)
    else:
        return (30, 60)


def session_duration_minutes(profile: str) -> int:
    if profile == "high":
        return random.randint(25, 60)
    elif profile == "medium":
        return random.randint(15, 45)
    elif profile == "low":
        return random.randint(10, 30)
    else:
        return random.randint(5, 20)


# ============================================
# HELPER: Generar timestamps distribuidos
# ============================================

def random_timestamp_in_range(start: datetime, end: datetime) -> datetime:
    """Genera un timestamp aleatorio dentro del rango."""
    diff = (end - start).total_seconds()
    return start + timedelta(seconds=random.randint(0, int(diff)))


def generate_weekly_sessions(
    student_id,
    game_id: uuid.UUID,
    profile: str,
    course_ids: List[uuid.UUID],
) -> List[Dict]:
    """
    Genera sesiones de juego distribuidas en la semana para 5 meses.
    Retorna lista de dicts con metadata de sesión.
    """
    sessions = []
    current = DATA_START
    week_count = 0

    while current < DATA_END:
        # Determinar si esta semana tiene actividad
        sessions_this_week = sessions_per_week(profile)
        if sessions_this_week == 0:
            current += timedelta(days=7)
            week_count += 1
            continue

        # Días de la semana con más actividad (lunes-jueves más que viernes-domingo)
        day_weights = [0.8, 0.9, 1.0, 0.9, 0.6, 0.3, 0.2]  # lun=0, dom=6
        available_days = list(range(7))
        chosen_days = random.choices(available_days, weights=day_weights, k=sessions_this_week)
        chosen_days = list(set(chosen_days))  # unique days

        for day_offset in chosen_days:
            session_date = current + timedelta(days=day_offset)
            if session_date >= DATA_END:
                break

            # Horario realista: 8am-8pm, picos a media mañana y media tarde
            hour_weights = [0] * 24
            for h in range(8, 21):  # 8am a 8pm
                hour_weights[h] = 1.0
            # Picos
            for h in [9, 10, 11, 14, 15, 16]:
                hour_weights[h] = 2.0

            hour = random.choices(range(24), weights=hour_weights, k=1)[0]
            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            session_start = session_date.replace(
                hour=hour, minute=minute, second=second, microsecond=0
            )

            if session_start >= DATA_END:
                break

            duration = session_duration_minutes(profile)
            session_end = session_start + timedelta(minutes=duration)

            # Niveles a jugar (depende del perfil - los mejores juegan más niveles)
            if profile == "high":
                levels_played = random.randint(1, 4)
            elif profile == "medium":
                levels_played = random.randint(1, 3)
            elif profile == "low":
                levels_played = random.randint(1, 2)
            else:
                levels_played = 1

            sessions.append({
                "started_at": session_start,
                "ended_at": session_end,
                "duration_minutes": duration,
                "levels_played": levels_played,
                "student_id": student_id,
                "game_id": game_id,
                "course_id": random.choice(course_ids) if course_ids else None,
                "profile": profile,
            })

        current += timedelta(days=7)
        week_count += 1

    return sessions


# ============================================
# SEGMENT TEMPLATES for each level
# ============================================

def generate_segments_for_level(level: Level, level_idx: int, game_title: str):
    """
    Genera configuración de segmentos para un nivel.
    Retorna lista de (segment_number, configuration) tuples.
    """
    segments = []

    if game_title == "Matemáticas Interactivas":
        if level.level_number == 1:
            segments = [
                (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                     "description": "Sumas y restas simples"}),
                (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                     "description": "Multiplicaciones"}),
                (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                     "description": "Operaciones combinadas"}),
            ]
        elif level.level_number == 2:
            segments = [
                (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                     "description": "Ecuaciones lineales simples"}),
                (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                     "description": "Ecuaciones con paréntesis"}),
                (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                     "description": "Problemas de aplicación"}),
            ]
    elif game_title == "Programación Visual - Bloques":
        if level.level_number == 1:  # Variables
            segments = [
                (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                     "description": "Declaración de variables"}),
                (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                     "description": "Asignación y operaciones"}),
                (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                     "description": "Variables en expresiones"}),
            ]
        elif level.level_number == 2:  # Condicionales
            segments = [
                (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                     "description": "If simple"}),
                (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                     "description": "If-else"}),
                (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                     "description": "Condiciones anidadas"}),
            ]
        elif level.level_number == 3:  # Bucles
            segments = [
                (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                     "description": "Ciclo for simple"}),
                (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                     "description": "Ciclo while"}),
                (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                     "description": "Bucles anidados"}),
            ]
        elif level.level_number == 4:  # Funciones
            segments = [
                (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                     "description": "Definición de funciones"}),
                (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                     "description": "Funciones con parámetros"}),
                (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                     "description": "Funciones con retorno"}),
            ]

    return segments


# ============================================
# MAIN SEED FUNCTIONS
# ============================================

async def load_existing_data(db) -> dict:
    """Carga todos los datos existentes de la BD."""
    print("\n[Cargando datos existentes...]")

    # Roles
    roles = {}
    result = await db.execute(select(Role))
    for role in result.scalars().all():
        roles[role.role_name] = role
    print(f"  ✓ Roles: {list(roles.keys())}")

    # Games (except Hello World)
    result = await db.execute(select(Game).where(Game.is_deleted == False))
    games = {g.title: g for g in result.scalars().all()}

    hello_world = games.get(HELLO_WORLD_TITLE)
    target_games = {k: v for k, v in games.items() if k != HELLO_WORLD_TITLE}
    print(f"  ✓ Juegos: {list(games.keys())}")
    print(f"  ✓ Juegos target: {list(target_games.keys())}")

    # Levels for target games
    result = await db.execute(
        select(Level).where(
            Level.game_id.in_([g.id for g in target_games.values()]),
            Level.is_deleted == False,
        ).order_by(Level.game_id, Level.level_number)
    )
    levels = result.scalars().all()
    print(f"  ✓ Niveles target: {len(levels)}")

    # Group levels by game
    levels_by_game = defaultdict(list)
    for lvl in levels:
        levels_by_game[lvl.game_id].append(lvl)

    # SegmentLevels for target levels
    level_ids = [l.id for l in levels]
    result = await db.execute(
        select(SegmentLevel).where(
            SegmentLevel.level_number_id.in_(level_ids),
            SegmentLevel.is_deleted == False,
        )
    )
    existing_segments = result.scalars().all()
    existing_seg_map = defaultdict(set)
    for seg in existing_segments:
        existing_seg_map[seg.level_number_id].add(seg.segment_number)
    print(f"  ✓ Segmentos existentes: {len(existing_segments)}")

    # Users - students
    result = await db.execute(
        select(Student).options(selectinload(Student.user))
        .where(Student.is_deleted == False)
    )
    students = result.scalars().all()
    print(f"  ✓ Estudiantes: {len(students)}")

    # Professors
    result = await db.execute(
        select(Professor).options(selectinload(Professor.user))
        .where(Professor.is_deleted == False)
    )
    professors = result.scalars().all()
    print(f"  ✓ Profesores: {len(professors)}")

    # Courses - load all
    result = await db.execute(
        select(Course).where(Course.is_deleted == False)
    )
    courses = result.scalars().all()
    print(f"  ✓ Cursos: {len(courses)}")

    # Enrollments
    result = await db.execute(select(CourseEnrollment).where(CourseEnrollment.is_deleted == False))
    enrollments = result.scalars().all()
    enrollment_map = defaultdict(list)
    for e in enrollments:
        enrollment_map[e.student_id].append(e.course_id)
    print(f"  ✓ Enrollments: {len(enrollments)}")

    return {
        "roles": roles,
        "games": games,
        "hello_world": hello_world,
        "target_games": target_games,
        "levels": levels,
        "levels_by_game": levels_by_game,
        "existing_segments": existing_segments,
        "existing_seg_map": existing_seg_map,
        "students": students,
        "professors": professors,
        "courses": courses,
        "enrollments": enrollments,
        "enrollment_map": enrollment_map,
    }


async def add_missing_segments(db, data: dict):
    """Agrega segmentos faltantes a niveles existentes."""
    print("\n[Agregando segmentos faltantes...]")

    count = 0
    for game_title, game in data["target_games"].items():
        for level in data["levels_by_game"].get(game.id, []):
            existing_nums = data["existing_seg_map"].get(level.id, set())
            segments = generate_segments_for_level(level, level.level_number, game_title)

            for seg_num, config in segments:
                if seg_num not in existing_nums:
                    segment = SegmentLevel(
                        level_number_id=level.id,
                        segment_number=seg_num,
                        configuration=config,
                    )
                    db.add(segment)
                    count += 1
                    print(f"  ✓ Segmento {seg_num} para '{level.title}' ({game_title})")

    if count > 0:
        await db.commit()
        print(f"\n✓ {count} segmentos creados")

        # Recargar segmentos
        level_ids = [l.id for l in data["levels"]]
        result = await db.execute(
            select(SegmentLevel).where(
                SegmentLevel.level_number_id.in_(level_ids),
                SegmentLevel.is_deleted == False,
            )
        )
        data["all_segments"] = result.scalars().all()

        # Index by level
        data["segments_by_level"] = defaultdict(list)
        for seg in data["all_segments"]:
            data["segments_by_level"][seg.level_number_id].append(seg)

        # Also index by (level_id, segment_number)
        data["segment_map"] = {}
        for seg in data["all_segments"]:
            key = (seg.level_number_id, seg.segment_number)
            data["segment_map"][key] = seg
    else:
        print("  ✓ No faltan segmentos")

        # If we didn't create any, they're already in existing_segments
        level_ids = [l.id for l in data["levels"]]
        result = await db.execute(
            select(SegmentLevel).where(
                SegmentLevel.level_number_id.in_(level_ids),
                SegmentLevel.is_deleted == False,
            )
        )
        data["all_segments"] = result.scalars().all()

        data["segments_by_level"] = defaultdict(list)
        for seg in data["all_segments"]:
            data["segments_by_level"][seg.level_number_id].append(seg)

        data["segment_map"] = {}
        for seg in data["all_segments"]:
            key = (seg.level_number_id, seg.segment_number)
            data["segment_map"][key] = seg

    return data


async def assign_games_to_courses(db, data: dict):
    """Asigna juegos a cursos que no tienen game_id."""
    print("\n[Asignando juegos a cursos...]")

    count = 0
    for course_name, game_title in COURSE_GAME_ASSIGNMENTS:
        game = data["target_games"].get(game_title)
        if not game:
            continue

        # Find courses matching this name (case-insensitive partial match)
        for course in data["courses"]:
            if course.game_id is not None:
                continue  # Ya tiene juego
            if course_name.lower() in course.name.lower():
                course.game_id = game.id
                db.add(course)
                count += 1
                print(f"  ✓ '{course.name}' → {game_title}")

    if count > 0:
        await db.commit()
        print(f"\n✓ {count} cursos asignados")
    else:
        print("  ✓ No hay cursos para asignar")

    return data


async def generate_gameplay_data(db, data: dict):
    """Genera TODOS los datos de juego, progreso, xAPI y sync para Feb-Jun 2026."""
    print("\n[Generando datos de juego Feb-Jun 2026...]")

    # Pre-load student user data
    students_with_users = (await db.execute(
        select(Student).options(selectinload(Student.user))
        .where(Student.is_deleted == False)
    )).scalars().all()

    if not data["target_games"] or not data.get("all_segments"):
        print("✗ Faltan juegos target o segmentos")
        return

    all_games_list = list(data["target_games"].values())
    all_segments = data["all_segments"]
    segments_by_level = data["segments_by_level"]

    total_instances = 0
    total_progress = 0
    total_xapi = 0
    total_sync_sessions = 0
    total_sync_events = 0

    for student in students_with_users:
        profile = assign_profile()
        student_courses = data["enrollment_map"].get(student.id, [])
        course_ids = student_courses if student_courses else []

        # Cada estudiante juega 1-2 juegos target
        games_for_student = random.sample(
            all_games_list,
            k=min(random.randint(1, 2), len(all_games_list))
        )

        for game in games_for_student:
            game_levels = data["levels_by_game"].get(game.id, [])
            if not game_levels:
                continue

            # Generar sesiones semanales para 5 meses
            sessions = generate_weekly_sessions(
                student.id, game.id, profile, course_ids
            )
            total_sync_sessions += len(sessions)

            for sess in sessions:
                # Crear game_instance
                instance = GameInstance(
                    started_at=sess["started_at"],
                    ended_at=sess["ended_at"],
                    status="completed",
                    student_id=sess["student_id"],
                    game_id=sess["game_id"],
                    course_id=sess.get("course_id"),
                )
                db.add(instance)
                await db.flush()
                total_instances += 1

                # Crear sync_session
                sync_session = SyncSession(
                    start_time=sess["started_at"],
                    end_time=sess["ended_at"],
                    status="completed",
                    instance_id=instance.id,
                )
                db.add(sync_session)
                await db.flush()

                # Eventos de sync para esta sesión
                num_events = random.randint(6, 20)
                levels_accessed = random.sample(
                    game_levels,
                    k=min(sess["levels_played"], len(game_levels))
                )

                for i in range(num_events):
                    event_time = sess["started_at"] + timedelta(
                        seconds=random.randint(0, sess["duration_minutes"] * 60 - 1)
                    )
                    event_type = random.choice(SYNC_EVENT_TYPES)

                    event_level = random.choice(levels_accessed) if levels_accessed else random.choice(game_levels)

                    payload = {
                        "level_id": str(event_level.id),
                        "level_number": event_level.level_number,
                        "timestamp": event_time.isoformat(),
                    }

                    if "completed" in event_type:
                        score_min, score_max = score_range(profile)
                        payload["score"] = random.randint(score_min, score_max)
                        payload["duration_seconds"] = random.randint(30, 300)

                    if "error" in event_type:
                        payload["error_message"] = random.choice([
                            "Syntax error", "Type mismatch",
                            "Missing block", "Wrong order"
                        ])
                        payload["error_line"] = random.randint(1, 15)

                    if "hint" in event_type:
                        payload["hint_id"] = random.randint(1, 5)

                    sync_event = SyncEvent(
                        event_type=event_type,
                        payload=payload,
                        timestamp=event_time,
                        status="processed" if random.random() > 0.15 else "pending",
                        sync_session_id=sync_session.id,
                    )
                    db.add(sync_event)
                    total_sync_events += 1

                    # Progreso (1 de cada 2-3 eventos genera progress, o en level.completed)
                    create_progress = (
                        "completed" in event_type
                        or ("segment" in event_type)
                        or (i % 3 == 0 and random.random() > 0.5)
                    )

                    if create_progress:
                        segment = None
                        if event_level.id in segments_by_level:
                            segments = segments_by_level[event_level.id]
                            if segments:
                                segment = random.choice(segments)

                        if segment:
                            att_min, att_max = attempts_range(profile)
                            h_min, h_max = hints_range(profile)
                            eff_min, eff_max = efficiency_range(profile)
                            s_min, s_max = score_range(profile)

                            eff = random.randint(eff_min, eff_max)
                            progress = Progress(
                                attempt_count=random.randint(att_min, att_max),
                                error_count=random.randint(0, 3) if profile in ["low", "inactive"] else random.randint(0, 1),
                                hints_used_count=random.randint(h_min, h_max),
                                errors_details={"errors": []},
                                objectives_completed=random.randint(1, 5),
                                efficiency_rating=eff,
                                student_id=student.id,
                                segment_level_id=segment.id,
                                created_at=event_time,
                            )
                            db.add(progress)
                            total_progress += 1

                    # xAPI statements (1 de cada 1.5 eventos)
                    if random.random() > 0.35:
                        verb_key = random.choice(list(XAPI_VERBS.keys()))
                        verb_data = XAPI_VERBS[verb_key]
                        stmt_id = str(uuid.uuid4())

                        s_min, s_max = score_range(profile)

                        xapi = XAPIStatement(
                            id=stmt_id,
                            actor_mbox=f"mailto:{student.user.email}",
                            actor_account_name=student.user.username,
                            actor_account_homepage="https://game.helloworld.edu",
                            verb_id=verb_data["id"],
                            verb_display=verb_data["display"],
                            object_id=f"https://game.helloworld.edu/activities/level/{event_level.id}",
                            object_type="Activity",
                            object_definition_type="http://adlnet.gov/expapi/activities/level",
                            object_definition_name={"en-US": event_level.title},
                            platform="Godot Game Client",
                            language="es",
                            context_extensions={
                                "profile": profile,
                                "session_duration": sess["duration_minutes"],
                            },
                            result_score_raw=str(random.randint(s_min, s_max)),
                            result_score_min="0",
                            result_score_max="100",
                            result_score_scaled=str(random.randint(s_min, s_max) / 100),
                            result_success=(verb_key == "completed"),
                            result_completion=(verb_key == "completed"),
                            result_duration=f"PT{random.randint(5, 30)}M",
                            timestamp=event_time,
                            stored=event_time,
                            statement={},
                            student_id=student.id,
                            game_id=game.id,
                            level_id=event_level.id,
                        )
                        db.add(xapi)
                        total_xapi += 1

                # Commit cada ~20 estudiantes para no saturar
                if total_instances % 500 == 0:
                    await db.commit()
                    print(f"  ... {total_instances} instancias, {total_progress} progresos, {total_xapi} xAPI generados...")

    # Commit final
    await db.commit()
    print(f"\n✓ Datos generados:")
    print(f"  - Instancias de juego: {total_instances}")
    print(f"  - Sesiones sync: {total_sync_sessions}")
    print(f"  - Eventos sync: {total_sync_events}")
    print(f"  - Progresos: {total_progress}")
    print(f"  - Statements xAPI: {total_xapi}")

    return {
        "total_instances": total_instances,
        "total_sync_sessions": total_sync_sessions,
        "total_sync_events": total_sync_events,
        "total_progress": total_progress,
        "total_xapi": total_xapi,
    }


async def generate_feedbacks(db, data: dict, stats: dict = None):
    """Genera feedbacks realistas de estudiantes."""
    print("\n[Generando feedbacks...]")

    comments_by_rating = {
        5: [
            "Excelente curso, muy bien estructurado y dinámico",
            "Me encantó la forma de aprender jugando",
            "El profesor explica muy claro, aprendí mucho",
            "Los ejercicios prácticos son fantasticos",
            "Recomiendo este curso a todos mis compañeros",
        ],
        4: [
            "Muy buen curso, contenido de calidad",
            "Las clases son entretenidas y educativas",
            "Buen material de apoyo y ejercicios",
            "El ritmo de la clase es adecuado",
            "Me gustó la interacción en clase",
        ],
        3: [
            "Curso aceptable, algunas areas por mejorar",
            "El contenido es bueno pero falta práctica",
            "Podrian tener más ejercicios de ejemplo",
            "La teoría está bien, pero muy rapido a veces",
            "Esperaba más niveles en el juego",
        ],
    }

    comments_flat = []
    for rating, cmts in comments_by_rating.items():
        for c in cmts:
            comments_flat.append((rating, c))

    feedbacks_count = 0
    students_with_users = (await db.execute(
        select(Student).options(selectinload(Student.user))
        .where(Student.is_deleted == False)
    )).scalars().all()

    professors = data["professors"]

    if not professors:
        print("  ✗ No hay profesores para feedbacks")
        return

    # ~60% de los estudiantes dejan feedback
    for student in students_with_users:
        if random.random() > 0.6:
            continue

        num_feedbacks = random.randint(1, 2)
        for _ in range(num_feedbacks):
            professor = random.choice(professors)

            # Buscar cursos donde el estudiante y profesor coincidan
            student_courses = data["enrollment_map"].get(student.id, [])
            course_id = random.choice(student_courses) if student_courses else None

            rating, comment = random.choice(comments_flat)
            # Variar un poco el rating
            rating = max(1, min(5, rating + random.randint(-1, 1)))

            feedback = Feedback(
                comments=comment,
                rating=rating,
                student_id=student.id,
                professor_id=professor.id,
                course_id=course_id,
            )
            db.add(feedback)
            feedbacks_count += 1

    await db.commit()
    print(f"✓ {feedbacks_count} feedbacks generados")

    return feedbacks_count


async def print_data_summary(db):
    """Imprime resumen final de la BD."""
    print("\n" + "=" * 55)
    print("RESUMEN FINAL DE DATOS EN BD")
    print("=" * 55)

    tables = [
        ("students", Student),
        ("professors", Professor),
        ("courses", Course),
        ("course_enrollments", CourseEnrollment),
        ("games", Game),
        ("levels", Level),
        ("segment_levels", SegmentLevel),
        ("game_instances", GameInstance),
        ("progresses", Progress),
        ("xapi_statements", XAPIStatement),
        ("sync_sessions", SyncSession),
        ("sync_events", SyncEvent),
        ("feedbacks", Feedback),
    ]

    for name, model in tables:
        try:
            result = await db.execute(select(model).where(model.is_deleted == False))
            count = len(result.scalars().all())
            print(f"  {name:<25} {count:>8}")
        except Exception:
            print(f"  {name:<25} {'ERROR':>8}")

    # Mostrar rangos de fecha
    for label, model, col in [
        ("Rango game_instances", GameInstance, GameInstance.started_at),
        ("Rango xapi_statements", XAPIStatement, XAPIStatement.timestamp),
        ("Rango sync_sessions", SyncSession, SyncSession.start_time),
    ]:
        try:
            result = await db.execute(select(col).order_by(col).limit(1))
            min_val = result.scalar()
            result = await db.execute(select(col).order_by(col.desc()).limit(1))
            max_val = result.scalar()
            if min_val:
                print(f"  {label:<25} {min_val.date()} → {max_val.date()}")
        except Exception:
            pass

    print("=" * 55)


async def main():
    """Ejecuta todo el seed."""
    print("\n" + "=" * 55)
    print("SEED DE DATOS REALISTAS - Hello World Project")
    print("Febrero a Junio 2026 - 5 meses de datos")
    print("=" * 55 + "\n")

    db = SessionLocal()
    try:
        # 1. Cargar datos existentes
        data = await load_existing_data(db)

        if not data["target_games"]:
            print("\n✗ ERROR: No se encontraron juegos target (Matemáticas Interactivas y Programación Visual)")
            print("  Asegurate de que existan en la BD antes de ejecutar este seed.")
            return

        # 2. Agregar segmentos faltantes
        data = await add_missing_segments(db, data)

        # 3. Asignar juegos a cursos
        data = await assign_games_to_courses(db, data)

        # 4. Generar datos de juego (instancias, progreso, xAPI, sync)
        stats = await generate_gameplay_data(db, data)

        # 5. Generar feedbacks
        feedbacks_count = await generate_feedbacks(db, data, stats)

        # 6. Mostrar resumen
        await print_data_summary(db)

        print(f"\n✓ SEED COMPLETADO EXITOSAMENTE!")
        print(f"  Período: {DATA_START.date()} → {DATA_END.date()}")
        print(f"  Estudiantes: {len(data['students'])}")
        print(f"  Juegos target: {list(data['target_games'].keys())}")
        print(f"  Cursos con juego asignado: {sum(1 for c in data['courses'] if c.game_id)}")

    except Exception as e:
        await db.rollback()
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
