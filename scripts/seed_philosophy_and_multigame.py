#!/usr/bin/env python3
"""
Seed complementario: Agrega juego de Filosofía + datos multi-juego para algunos estudiantes.

Reemplaza "Programación Visual - Bloques" por "Filosofía y Pensamiento Crítico":
- 4 niveles: Lógica, Ética, Epistemología, Metafísica
- 3 segmentos por nivel
- Reasigna cursos de Prog. Visual → Filosofía
- Genera datos Feb-Jun 2026 para Filosofía
- Agrega datos multi-juego (algunos estudiantes juegan Hello World + otros juegos)

USO:
    cd apps/backend && uv run python ../../scripts/seed_philosophy_and_multigame.py

NO borra datos existentes.
"""

import asyncio
import random
import uuid
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict

# Path setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "apps" / "backend" / "src"
sys.path.insert(0, str(BACKEND_DIR))
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Load .env
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
                val = val.replace("@postgresql_db:", "@localhost:")
                val = val.replace("@postgres:", "@localhost:")
            if key not in os.environ:
                os.environ[key] = val

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.shared.infrastructure.session import SessionLocal
from src.users.domain.user import User
from src.users.domain.role import Role
from src.users.domain.professor import Professor
from src.users.domain.student import Student
from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment
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
# CONSTANTES
# ============================================

OLD_GAME_TITLE = "Programación Visual - Bloques"
NEW_GAME_TITLE = "Filosofía y Pensamiento Crítico"
HELLO_WORLD_TITLE = "Hello World"
MATH_GAME_TITLE = "Matemáticas Interactivas"

LEVELS_DATA = [
    {
        "level_number": 1,
        "title": "Lógica",
        "description": "Principios de razonamiento válido",
        "goal": "Aplicar reglas lógicas básicas",
        "segments": [
            (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                 "description": "Proposiciones y valores de verdad"}),
            (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                 "description": "Conectivos lógicos (y, o, no)"}),
            (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                 "description": "Tablas de verdad"}),
        ]
    },
    {
        "level_number": 2,
        "title": "Ética",
        "description": "Teorías éticas y dilemas morales",
        "goal": "Analizar dilemas éticos usando diferentes marcos",
        "segments": [
            (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                 "description": "Introducción a la ética"}),
            (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                 "description": "Ética deontológica vs consecuencialista"}),
            (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                 "description": "Análisis de dilemas morales"}),
        ]
    },
    {
        "level_number": 3,
        "title": "Epistemología",
        "description": "Teoría del conocimiento",
        "goal": "Distinguir entre creencia, justificación y conocimiento",
        "segments": [
            (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                 "description": "¿Qué es el conocimiento?"}),
            (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                 "description": "Racionalismo vs empirismo"}),
            (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                 "description": "El problema de la inducción"}),
        ]
    },
    {
        "level_number": 4,
        "title": "Metafísica",
        "description": "Naturaleza de la realidad",
        "goal": "Explorar conceptos ontológicos fundamentales",
        "segments": [
            (1, {"type": "exercise_1", "count": 5, "difficulty": "basic",
                 "description": "Ser y existencia"}),
            (2, {"type": "exercise_2", "count": 4, "difficulty": "intermediate",
                 "description": "Mente-cuerpo y dualismo"}),
            (3, {"type": "exercise_3", "count": 3, "difficulty": "advanced",
                 "description": "Libre albedrío vs determinismo"}),
        ]
    },
]

DATA_START = datetime(2026, 2, 1, 8, 0, 0)
DATA_END = datetime(2026, 6, 23, 18, 0, 0)

SYNC_EVENT_TYPES = [
    "game.started", "level.started", "level.completed", "level.failed",
    "block.placed", "block.removed", "hint.requested", "error.created",
    "error.corrected", "segment.completed", "game.completed",
    "choice.selected", "argument.analyzed",
]

XAPI_VERBS = {
    "interacted": {"id": "http://adlnet.gov/expapi/verbs/interacted", "display": {"en-US": "interacted"}},
    "completed": {"id": "http://adlnet.gov/expapi/verbs/completed", "display": {"en-US": "completed"}},
    "attempted": {"id": "http://adlnet.gov/expapi/verbs/attempted", "display": {"en-US": "attempted"}},
    "progressed": {"id": "http://adlnet.gov/expapi/verbs/progressed", "display": {"en-US": "progressed"}},
}

PROFILE_TYPES = ["high", "medium", "low", "inactive"]
PROFILE_WEIGHTS = [0.2, 0.5, 0.2, 0.1]


def assign_profile() -> str:
    return random.choices(PROFILE_TYPES, weights=PROFILE_WEIGHTS, k=1)[0]


def sessions_per_week(profile: str) -> int:
    return {"high": (3, 5), "medium": (2, 4), "low": (1, 2), "inactive": (0, 1)}[profile]
def sess_range(p):
    r = sessions_per_week(p)
    return random.randint(r[0], r[1]) if isinstance(r, tuple) else r


def score_range(profile: str) -> tuple:
    return {"high": (80, 100), "medium": (55, 90), "low": (30, 70), "inactive": (20, 60)}[profile]


def attempts_range(profile: str) -> tuple:
    return {"high": (1, 2), "medium": (2, 5), "low": (4, 8), "inactive": (1, 3)}[profile]


def hints_range(profile: str) -> tuple:
    return {"high": (0, 1), "medium": (1, 3), "low": (2, 5), "inactive": (0, 2)}[profile]


def efficiency_range(profile: str) -> tuple:
    return {"high": (85, 100), "medium": (60, 90), "low": (35, 65), "inactive": (30, 60)}[profile]


def session_duration_minutes(profile: str) -> int:
    d = {"high": (25, 60), "medium": (15, 45), "low": (10, 30), "inactive": (5, 20)}
    return random.randint(*d[profile])


def random_timestamp_in_range(start: datetime, end: datetime) -> datetime:
    diff = (end - start).total_seconds()
    return start + timedelta(seconds=random.randint(0, int(diff)))


# ============================================
# HELPERS
# ============================================

def generate_weekly_sessions(student_id, game_id, profile, course_ids, sessions_multiplier=1.0):
    """Genera sesiones semanales distribuidas en Feb-Jun 2026."""
    sessions = []
    current = DATA_START

    while current < DATA_END:
        s_range = sessions_per_week(profile)
        num = max(1, int(s_range[0] * sessions_multiplier)) if random.random() > 0.2 else 0
        if num == 0:
            current += timedelta(days=7)
            continue

        day_weights = [0.8, 0.9, 1.0, 0.9, 0.6, 0.3, 0.2]
        available_days = list(range(7))
        chosen_days = random.choices(available_days, weights=day_weights, k=num)
        chosen_days = list(set(chosen_days))

        for day_offset in chosen_days:
            session_date = current + timedelta(days=day_offset)
            if session_date >= DATA_END:
                break

            hour = random.choices(range(24), weights=[0]*8 + [1]*13 + [0]*3, k=1)[0]
            session_start = session_date.replace(hour=hour, minute=random.randint(0, 59),
                                                  second=random.randint(0, 59), microsecond=0)
            if session_start >= DATA_END:
                break

            duration = session_duration_minutes(profile)
            session_end = session_start + timedelta(minutes=duration)

            sessions.append({
                "started_at": session_start,
                "ended_at": session_end,
                "duration_minutes": duration,
                "levels_played": random.randint(1, 3),
                "student_id": student_id,
                "game_id": game_id,
                "course_id": random.choice(course_ids) if course_ids else None,
                "profile": profile,
            })

        current += timedelta(days=7)

    return sessions


async def create_session_data(db, student, game, levels, segments_by_level, course_ids, profile,
                              sessions, total_counters):
    """Crea una sesión de juego con todos sus datos asociados."""
    for sess in sessions:
        instance = GameInstance(
            started_at=sess["started_at"], ended_at=sess["ended_at"],
            status="completed", student_id=sess["student_id"],
            game_id=sess["game_id"], course_id=sess.get("course_id"),
        )
        db.add(instance)
        await db.flush()  # ← obtener instance.id
        total_counters["instances"] += 1

        sync_session = SyncSession(
            start_time=sess["started_at"], end_time=sess["ended_at"],
            status="completed", instance_id=instance.id,
        )
        db.add(sync_session)
        await db.flush()  # ← obtener sync_session.id
        db.add(sync_session)
        total_counters["sync_sessions"] += 1

        num_events = random.randint(6, 18)
        level = random.choice(levels) if levels else None

        for i in range(num_events):
            event_time = sess["started_at"] + timedelta(
                seconds=random.randint(0, max(1, sess["duration_minutes"] * 60 - 1))
            )
            event_type = random.choice(SYNC_EVENT_TYPES)
            payload = {
                "level_number": level.level_number if level else 1,
                "timestamp": event_time.isoformat(),
            }
            if "completed" in event_type:
                s_min, s_max = score_range(profile)
                payload["score"] = random.randint(s_min, s_max)
            if "error" in event_type:
                payload["error_message"] = random.choice(["Error de sintaxis", "Tipo incorrecto", "Orden inválido"])
                payload["error_line"] = random.randint(1, 10)

            sync_event = SyncEvent(
                event_type=event_type, payload=payload, timestamp=event_time,
                status="processed" if random.random() > 0.15 else "pending",
                sync_session_id=sync_session.id,
            )
            db.add(sync_event)
            total_counters["sync_events"] += 1

            # Progress
            create_progress = ("completed" in event_type or "segment" in event_type or i % 3 == 0)
            if create_progress and level and level.id in segments_by_level:
                segments = segments_by_level[level.id]
                if segments and random.random() > 0.3:
                    segment = random.choice(segments)
                    att_min, att_max = attempts_range(profile)
                    h_min, h_max = hints_range(profile)
                    eff_min, eff_max = efficiency_range(profile)

                    progress = Progress(
                        attempt_count=random.randint(att_min, att_max),
                        error_count=random.randint(0, 2),
                        hints_used_count=random.randint(h_min, h_max),
                        errors_details={"errors": []},
                        objectives_completed=random.randint(1, 5),
                        efficiency_rating=random.randint(eff_min, eff_max),
                        student_id=student.id,
                        segment_level_id=segment.id,
                        created_at=event_time,
                    )
                    db.add(progress)
                    total_counters["progress"] += 1

            # xAPI
            if random.random() > 0.35:
                verb_key = random.choice(list(XAPI_VERBS.keys()))
                verb_data = XAPI_VERBS[verb_key]
                s_min, s_max = score_range(profile)
                xapi = XAPIStatement(
                    id=str(uuid.uuid4()),
                    actor_mbox=f"mailto:{student.user.email}",
                    actor_account_name=student.user.username,
                    actor_account_homepage="https://game.helloworld.edu",
                    verb_id=verb_data["id"],
                    verb_display=verb_data["display"],
                    object_id=f"https://game.helloworld.edu/activities/level/{level.id if level else 'unknown'}",
                    object_type="Activity",
                    object_definition_type="http://adlnet.gov/expapi/activities/level",
                    object_definition_name={"en-US": level.title if level else game.title},
                    platform="Godot Game Client", language="es",
                    context_extensions={"profile": profile, "session_duration": sess["duration_minutes"]},
                    result_score_raw=str(random.randint(s_min, s_max)),
                    result_score_min="0", result_score_max="100",
                    result_score_scaled=str(random.randint(s_min, s_max) / 100),
                    result_success=(verb_key == "completed"),
                    result_completion=(verb_key == "completed"),
                    result_duration=f"PT{random.randint(5, 30)}M",
                    timestamp=event_time, stored=event_time, statement={},
                    student_id=student.id, game_id=game.id,
                    level_id=level.id if level else None,
                )
                db.add(xapi)
                total_counters["xapi"] += 1

    return total_counters


# ============================================
# MAIN
# ============================================

async def main():
    print("\n" + "=" * 55)
    print("SEED FILOSOFÍA + MULTI-JUEGO")
    print("=" * 55 + "\n")

    db = SessionLocal()
    try:
        # ─── CARGAR DATOS EXISTENTES ───────────────────────
        print("[Cargando datos existentes...]")

        result = await db.execute(select(Game).where(Game.is_deleted == False))
        games = {g.title: g for g in result.scalars().all()}

        result = await db.execute(
            select(Student).options(selectinload(Student.user))
            .where(Student.is_deleted == False)
        )
        students = result.scalars().all()
        print(f"  Estudiantes: {len(students)}")

        old_game = games.get(OLD_GAME_TITLE)
        hello_world = games.get(HELLO_WORLD_TITLE)
        math_game = games.get(MATH_GAME_TITLE)

        if not old_game:
            print(f"  ✗ No se encontró '{OLD_GAME_TITLE}'. Nada que reemplazar.")
            return

        # ─── 1. CREAR JUEGO DE FILOSOFÍA ──────────────────
        print(f"\n[1. Creando '{NEW_GAME_TITLE}'...]")

        # Check if it already exists
        existing = await db.execute(
            select(Game).where(Game.title == NEW_GAME_TITLE, Game.is_deleted == False)
        )
        philosophy_game = existing.scalar_one_or_none()

        if not philosophy_game:
            philosophy_game = Game(
                title=NEW_GAME_TITLE,
                description="Principios de filosofía y pensamiento crítico",
                creator="System",
                subject="Philosophy",
                publication_status="published",
            )
            db.add(philosophy_game)
            await db.flush()
            print(f"  ✓ Juego creado: {NEW_GAME_TITLE}")

            # Crear niveles + segmentos
            philosophy_levels = []
            all_segments = []
            for ldata in LEVELS_DATA:
                level = Level(
                    level_number=ldata["level_number"],
                    title=ldata["title"],
                    description=ldata["description"],
                    goal=ldata["goal"],
                    game_id=philosophy_game.id,
                )
                db.add(level)
                await db.flush()
                philosophy_levels.append(level)

                for seg_num, seg_config in ldata["segments"]:
                    segment = SegmentLevel(
                        level_number_id=level.id,
                        segment_number=seg_num,
                        configuration=seg_config,
                    )
                    db.add(segment)
                    all_segments.append(segment)

            await db.flush()
            print(f"  ✓ {len(philosophy_levels)} niveles creados:")
            for l in philosophy_levels:
                print(f"    · Nivel {l.level_number}: {l.title}")
            print(f"  ✓ {len(all_segments)} segmentos creados")
        else:
            print(f"  ✓ Ya existe: {NEW_GAME_TITLE}")

            # Load existing levels
            result = await db.execute(
                select(Level).where(Level.game_id == philosophy_game.id, Level.is_deleted == False)
                .order_by(Level.level_number)
            )
            philosophy_levels = result.scalars().all()

            result = await db.execute(
                select(SegmentLevel).where(
                    SegmentLevel.level_number_id.in_([l.id for l in philosophy_levels]),
                    SegmentLevel.is_deleted == False,
                )
            )
            all_segments = result.scalars().all()

        # ─── 2. REASIGNAR CURSOS ───────────────────────────
        print(f"\n[2. Reasignando cursos de '{OLD_GAME_TITLE}' → '{NEW_GAME_TITLE}'...]")

        result = await db.execute(
            select(Course).where(Course.game_id == old_game.id, Course.is_deleted == False)
        )
        courses_to_update = result.scalars().all()
        course_ids = [c.id for c in courses_to_update]

        for course in courses_to_update:
            course.game_id = philosophy_game.id
            db.add(course)

        if courses_to_update:
            await db.flush()
            print(f"  ✓ {len(courses_to_update)} cursos reasignados:")
            for c in courses_to_update:
                print(f"    · {c.name}")
        else:
            print(f"  ✓ No hay cursos que reasignar")

        # ─── 3. GENERAR DATOS DE FILOSOFÍA ─────────────────
        # (solo si es nuevo - para no duplicar si ya se ejecutó)
        print(f"\n[3. Generando datos de juego para '{NEW_GAME_TITLE}'...]")

        # Check if there's already data
        result = await db.execute(
            select(GameInstance).where(
                GameInstance.game_id == philosophy_game.id,
                GameInstance.is_deleted == False,
            ).limit(1)
        )
        already_has_data = result.scalar_one_or_none() is not None

        if already_has_data:
            print(f"  ✓ Ya tiene datos generados anteriormente")
        else:
            # Get segments grouped by level
            result = await db.execute(
                select(SegmentLevel).where(
                    SegmentLevel.level_number_id.in_([l.id for l in philosophy_levels]),
                    SegmentLevel.is_deleted == False,
                )
            )
            segs = result.scalars().all()
            segs_by_level = defaultdict(list)
            for s in segs:
                segs_by_all_level = {}
                segs_by_all_level[s.level_number_id] = segs_by_all_level.get(s.level_number_id, [])
                segs_by_all_level[s.level_number_id].append(s)
            segs_by_level = defaultdict(list)
            for s in segs:
                segs_by_level[s.level_number_id].append(s)

            # Load enrollments
            result = await db.execute(
                select(CourseEnrollment).where(
                    CourseEnrollment.course_id.in_(course_ids),
                    CourseEnrollment.is_deleted == False,
                )
            )
            enrollments = result.scalars().all()
            enrolled_student_ids = {e.student_id for e in enrollments}
            print(f"  Estudiantes en cursos de filosofía: {len(enrolled_student_ids)}")

            counters = {"instances": 0, "sync_sessions": 0, "sync_events": 0, "progress": 0, "xapi": 0}

            for student in students:
                if student.id not in enrolled_student_ids and random.random() > 0.4:
                    continue  # Skip if not enrolled (but 60% still play anyway)

                profile = assign_profile()

                # Get student's course IDs
                student_course_ids = [
                    e.course_id for e in enrollments if e.student_id == student.id
                ] if student.id in enrolled_student_ids else course_ids[:1]

                session_count_factor = 0.7 if student.id not in enrolled_student_ids else 1.0

                sessions = generate_weekly_sessions(
                    student.id, philosophy_game.id, profile,
                    student_course_ids, session_count_factor
                )

                counters = await create_session_data(
                    db, student, philosophy_game, philosophy_levels,
                    segs_by_level, student_course_ids, profile, sessions, counters
                )

                if counters["instances"] % 500 == 0 and counters["instances"] > 0:
                    await db.commit()
                    print(f"  ... {counters['instances']} instancias generadas...")

            await db.commit()
            print(f"\n  ✓ Datos de filosofía generados:")
            print(f"    - Instancias: {counters['instances']}")
            print(f"    - Progresos: {counters['progress']}")
            print(f"    - xAPI: {counters['xapi']}")
            print(f"    - Eventos sync: {counters['sync_events']}")

        # ─── 4. DATOS MULTI-JUEGO (Hello World + otros) ────
        print(f"\n[4. Agregando datos multi-juego (alumnos en +2 juegos)...]")

        if not hello_world:
            print(f"  ✗ No se encontró Hello World")
        else:
            # Find students who already play only 1 game and add Hello World to them
            # Get existing instances per student
            all_game_ids = [g.id for g in games.values()]
            result = await db.execute(
                select(GameInstance.student_id, GameInstance.game_id)
                .where(
                    GameInstance.game_id.in_(all_game_ids),
                    GameInstance.is_deleted == False,
                    GameInstance.student_id.in_([s.id for s in students]),
                )
                .distinct()
            )
            existing_pairs = result.all()
            student_games = defaultdict(set)
            for s_id, g_id in existing_pairs:
                student_games[s_id].add(g_id)

            # Students who DON'T play Hello World yet → add it as 2nd/3rd game
            candidates = [
                s for s in students
                if hello_world.id not in student_games.get(s.id, set())
                and len(student_games.get(s.id, set())) >= 1
                and random.random() > 0.35  # 65% of eligible students
            ]

            print(f"  Candidatos para multi-juego: {len(candidates)} estudiantes")

            # Get HW levels + segments
            result = await db.execute(
                select(Level).where(Level.game_id == hello_world.id, Level.is_deleted == False)
                .order_by(Level.level_number)
            )
            hw_levels = result.scalars().all()

            result = await db.execute(
                select(SegmentLevel).where(
                    SegmentLevel.level_number_id.in_([l.id for l in hw_levels]),
                    SegmentLevel.is_deleted == False,
                )
            )
            hw_segs = result.scalars().all()
            hw_segs_by_level = defaultdict(list)
            for s in hw_segs:
                hw_segs_by_level[s.level_number_id].append(s)

            # Get HW courses
            result = await db.execute(
                select(Course).where(Course.game_id == hello_world.id, Course.is_deleted == False)
            )
            hw_courses = result.scalars().all()
            hw_course_ids = [c.id for c in hw_courses]

            mu_counters = {"instances": 0, "sync_sessions": 0, "sync_events": 0, "progress": 0, "xapi": 0}

            for student in candidates:
                profile = assign_profile()
                # For multi-game students: fewer sessions per week (they play other games too)
                sessions = generate_weekly_sessions(
                    student.id, hello_world.id, profile, hw_course_ids, sessions_multiplier=0.5
                )
                # Only take a subset of sessions (they don't play ALL their time on a 2nd game)
                sessions = random.sample(sessions, max(1, len(sessions) // 2))

                if not sessions:
                    continue

                student_course_ids = hw_course_ids[:1]
                mu_counters = await create_session_data(
                    db, student, hello_world, hw_levels,
                    hw_segs_by_level, student_course_ids, profile, sessions, mu_counters
                )

                if mu_counters["instances"] % 200 == 0 and mu_counters["instances"] > 0:
                    await db.commit()
                    print(f"  ... {mu_counters['instances']} instancias multi-juego...")

            # Also: add some students playing BOTH Philosophy AND Math (already existing)
            # Now they play both - but we already have data. Let's add HW to math-only students too
            math_only_candidates = [
                s for s in students
                if hello_world.id not in student_games.get(s.id, set())
                and math_game and math_game.id in student_games.get(s.id, set())
                and random.random() > 0.5
            ]
            print(f"  Estudiantes math→multi: {len(math_only_candidates)}")

            for student in math_only_candidates:
                profile = assign_profile()
                sessions = generate_weekly_sessions(
                    student.id, hello_world.id, profile, hw_course_ids, sessions_multiplier=0.4
                )
                sessions = random.sample(sessions, max(1, len(sessions) // 3))
                if not sessions:
                    continue
                mu_counters = await create_session_data(
                    db, student, hello_world, hw_levels,
                    hw_segs_by_level, hw_course_ids, profile, sessions, mu_counters
                )

            await db.commit()
            print(f"\n  ✓ Datos multi-juego generados:")
            print(f"    - Instancias: {mu_counters['instances']}")
            print(f"    - Progresos: {mu_counters['progress']}")
            print(f"    - xAPI: {mu_counters['xapi']}")
            print(f"    - Eventos sync: {mu_counters['sync_events']}")

        # ─── 5. RESUMEN ──────────────────────────────────────
        print(f"\n[5. Resumen final...]")

        tables = [
            ("students", Student), ("professors", Professor),
            ("courses", Course), ("course_enrollments", CourseEnrollment),
            ("games", Game), ("levels", Level),
            ("segment_levels", SegmentLevel), ("game_instances", GameInstance),
            ("progresses", Progress), ("xapi_statements", XAPIStatement),
            ("sync_sessions", SyncSession), ("sync_events", SyncEvent),
            ("feedbacks", Feedback),
        ]
        for name, model in tables:
            try:
                result = await db.execute(select(model).where(model.is_deleted == False))
                print(f"  {name:<25} {len(result.scalars().all()):>8}")
            except Exception:
                pass

        # Games summary
        print(f"\n  Juegos activos:")
        for g in games.values():
            result = await db.execute(
                select(GameInstance).where(GameInstance.game_id == g.id, GameInstance.is_deleted == False)
            )
            cnt = len(result.scalars().all())
            print(f"    · {g.title}: {cnt} instancias")

        # New game
        result = await db.execute(
            select(GameInstance).where(GameInstance.game_id == philosophy_game.id, GameInstance.is_deleted == False)
        )
        cnt = len(result.scalars().all())
        print(f"    · {NEW_GAME_TITLE}: {cnt} instancias")

        print(f"\n✓ COMPLETADO!")

    except Exception as e:
        await db.rollback()
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
