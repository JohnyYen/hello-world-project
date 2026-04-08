from src.statistic.domain.metric_type import MetricType
from src.statistic.domain.feedback import Feedback
from src.statistic.domain.progress import Progress
from src.statistic.domain.xapi_statement import XAPIStatement
from src.shared.infrastructure.session import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import json
import random
import uuid


async def seed_metric_types(db: AsyncSession):
    """Seed metric types."""

    metric_types_data = [
        {
            "name": "Accuracy",
            "code": "accuracy",
            "description": "Percentage of correct answers",
        },
        {
            "name": "Time Spent",
            "code": "time_spent",
            "description": "Total time spent on task",
        },
        {
            "name": "Attempts",
            "code": "attempts",
            "description": "Number of attempts to complete",
        },
        {
            "name": "Hints Used",
            "code": "hints_used",
            "description": "Number of hints used",
        },
        {
            "name": "Error Rate",
            "code": "error_rate",
            "description": "Percentage of errors made",
        },
        {
            "name": "Completion Rate",
            "code": "completion_rate",
            "description": "Task completion percentage",
        },
        {
            "name": "Engagement Score",
            "code": "engagement",
            "description": "Overall engagement level",
        },
    ]

    metric_types = []
    for data in metric_types_data:
        query = select(MetricType).where(MetricType.code == data["code"])
        existing = (await db.execute(query)).scalars().first()

        if existing:
            print(f"Metric type '{data['code']}' already exists")
            metric_types.append(existing)
            continue

        metric_type = MetricType(
            name=data["name"],
            code=data["code"],
            description=data["description"],
        )
        db.add(metric_type)
        metric_types.append(metric_type)
        print(f"Seeded metric type: {data['code']}")

    return metric_types


async def seed_feedbacks(db: AsyncSession):
    """Seed feedbacks from students to professors."""
    from src.users.domain.student import Student
    from src.users.domain.professor import Professor
    from src.game.domain.game import Game
    from src.game.domain.level import Level

    # Get students, professors, games, and levels
    students_query = select(Student).limit(10)
    students = (await db.execute(students_query)).scalars().all()

    professors_query = select(Professor).limit(5)
    professors = (await db.execute(professors_query)).scalars().all()

    games_query = select(Game).limit(3)
    games = (await db.execute(games_query)).scalars().all()

    levels_query = select(Level).limit(10)
    levels = (await db.execute(levels_query)).scalars().all()

    if not students or not professors:
        print("No students or professors found for feedbacks")
        return []

    comments = [
        "Excelente metodología de enseñanza, muy clara la explicación.",
        "El contenido es muy completo, me ayudó a entender mejor el tema.",
        "Buena interacción en clase, los ejercicios son muy prácticos.",
        "El material de apoyo es muy útil para el estudio.",
        "Gracias por la paciencia y las explicaciones detalladas.",
        "Los ejemplos son muy claros y facilitan el aprendizaje.",
        "Muy buen ritmo de clase, se entiende todo perfectamente.",
        "Las evaluaciones son justas y bien estructuradas.",
        "El professor es muy accesible para resolver dudas.",
        "Excelente curso, lo推荐的 a todos mis compañeros.",
    ]

    feedbacks = []
    for i in range(15):
        student = random.choice(students)
        professor = random.choice(professors)

        # Some feedbacks are for games/levels, some general
        has_game = random.choice([True, True, False])
        game = random.choice(games) if has_game and games else None
        level = random.choice(levels) if game and levels else None

        feedback = Feedback(
            comments=random.choice(comments),
            rating=random.randint(3, 5),
            student_id=student.id,
            professor_id=professor.id,
            game_id=game.id if game else None,
            level_id=level.id if level else None,
        )
        db.add(feedback)
        feedbacks.append(feedback)

    print(f"Seeded {len(feedbacks)} feedbacks")
    return feedbacks


async def seed_progress(db: AsyncSession):
    """Seed progress records for students in segments."""
    from src.users.domain.student import Student
    from src.game.domain.segment_level import SegmentLevel

    students_query = select(Student).limit(15)
    students = (await db.execute(students_query)).scalars().all()

    segments_query = select(SegmentLevel).limit(20)
    segments = (await db.execute(segments_query)).scalars().all()

    if not students or not segments:
        print("No students or segments found for progress")
        return []

    progresses = []
    for student in students:
        # Each student has progress in several segments
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
            db.add(progress)
            progresses.append(progress)

    print(f"Seeded {len(progresses)} progress records")
    return progresses


async def seed_xapi_statements(db: AsyncSession):
    """Seed xAPI statements from game client."""
    from src.users.domain.student import Student
    from src.game.domain.game import Game
    from src.game.domain.level import Level
    from src.game.domain.segment_level import SegmentLevel

    students_query = select(Student).limit(10)
    students = (await db.execute(students_query)).scalars().all()

    games_query = select(Game).limit(3)
    games = (await db.execute(games_query)).scalars().all()

    levels_query = select(Level).limit(10)
    levels = (await db.execute(levels_query)).scalars().all()

    segments_query = select(SegmentLevel).limit(15)
    segments = (await db.execute(segments_query)).scalars().all()

    if not students or not games:
        print("No students or games found for xAPI statements")
        return []

    # xAPI verbs
    verbs = [
        {
            "id": "http://adlnet.gov/expapi/verbs/initialized",
            "display": {"en-US": "initialized"},
        },
        {
            "id": "http://adlnet.gov/expapi/verbs/completed",
            "display": {"en-US": "completed"},
        },
        {"id": "http://adlnet.gov/expapi/verbs/passed", "display": {"en-US": "passed"}},
        {"id": "http://adlnet.gov/expapi/verbs/failed", "display": {"en-US": "failed"}},
        {
            "id": "http://adlnet.gov/expapi/verbs/answered",
            "display": {"en-US": "answered"},
        },
        {
            "id": "http://adlnet.gov/expapi/verbs/interacted",
            "display": {"en-US": "interacted"},
        },
    ]

    statements = []
    for i in range(50):
        student = random.choice(students)
        game = random.choice(games)
        level = random.choice(levels) if levels else None
        segment = random.choice(segments) if segments else None

        verb = random.choice(verbs)
        timestamp = datetime.now() - timedelta(
            days=random.randint(1, 30), hours=random.randint(0, 23)
        )

        # Create statement ID (UUID format)
        statement_id = f"{uuid.uuid4()}"

        statement = XAPIStatement(
            id=statement_id,
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
        db.add(statement)
        statements.append(statement)

    print(f"Seeded {len(statements)} xAPI statements")
    return statements
