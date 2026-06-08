from src.game.domain.game import Game
from src.game.domain.level import Level
from src.game.domain.segment_level import SegmentLevel
from src.game.domain.game_instance import GameInstance
from src.shared.infrastructure.session import AsyncSession
from src.shared.domain.enums import GameStatus
from sqlalchemy import select
from datetime import datetime, timedelta
import json


async def seed_games(db: AsyncSession):
    """Seed games with levels and segments."""

    games_data = [
        {
            "title": "Matemáticas Básicas",
            "description": "Aprende operaciones básicas de matemáticas de forma interactiva",
            "creator": "Dr. Juan Pérez",
            "subject": "Mathematics",
            "publication_status": "published",
            "download_link": "https://games.helloworld.edu/matematicas-basicas.zip",
            "levels": [
                {
                    "level_number": 1,
                    "title": "Suma y Resta",
                    "description": "Operaciones básicas de suma y resta",
                    "goal": "Completar 10 operaciones correctamente",
                    "segments": [
                        {
                            "configuration": {
                                "type": "addition",
                                "range": (1, 10),
                                "count": 5,
                            }
                        },
                        {
                            "configuration": {
                                "type": "subtraction",
                                "range": (1, 10),
                                "count": 5,
                            }
                        },
                    ],
                },
                {
                    "level_number": 2,
                    "title": "Multiplicación",
                    "description": "Aprende las tablas de multiplicar",
                    "goal": "Completar tabla del 1 al 5",
                    "segments": [
                        {
                            "configuration": {
                                "type": "multiplication",
                                "table": 1,
                                "count": 10,
                            }
                        },
                        {
                            "configuration": {
                                "type": "multiplication",
                                "table": 2,
                                "count": 10,
                            }
                        },
                        {
                            "configuration": {
                                "type": "multiplication",
                                "table": 3,
                                "count": 10,
                            }
                        },
                    ],
                },
                {
                    "level_number": 3,
                    "title": "División",
                    "description": "Operaciones de división básicas",
                    "goal": "Completar 10 divisiones correctamente",
                    "segments": [
                        {
                            "configuration": {
                                "type": "division",
                                "divisor_range": (1, 5),
                                "count": 10,
                            }
                        },
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
            "download_link": "https://games.helloworld.edu/quimica-introductoria.zip",
            "levels": [
                {
                    "level_number": 1,
                    "title": "Elementos Químicos",
                    "description": "Identifica los primeros 20 elementos",
                    "goal": "Reconocer 20 elementos de la tabla periódica",
                    "segments": [
                        {
                            "configuration": {
                                "type": "element_matching",
                                "elements": list(range(1, 11)),
                            }
                        },
                        {
                            "configuration": {
                                "type": "element_matching",
                                "elements": list(range(11, 21)),
                            }
                        },
                    ],
                },
                {
                    "level_number": 2,
                    "title": "Enlace Químico",
                    "description": "Aprende sobre tipos de enlaces",
                    "goal": "Identificar tipos de enlaces",
                    "segments": [
                        {
                            "configuration": {
                                "type": "bonding",
                                "bond_types": ["ionic", "covalent", "metallic"],
                            }
                        },
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
            "download_link": "https://games.helloworld.edu/fisica-fundamental.zip",
            "levels": [
                {
                    "level_number": 1,
                    "title": "Velocidad y Aceleración",
                    "description": "Introducción al movimiento",
                    "goal": "Calcular velocidad y aceleración",
                    "segments": [
                        {
                            "configuration": {
                                "type": "velocity_calc",
                                "difficulty": "basic",
                            }
                        },
                        {
                            "configuration": {
                                "type": "acceleration_calc",
                                "difficulty": "basic",
                            }
                        },
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
            "download_link": "https://games.helloworld.edu/biologia-celular.zip",
            "levels": [
                {
                    "level_number": 1,
                    "title": "Partes de la Célula",
                    "description": "Identifica los organelos celulares",
                    "goal": "Reconocer 15 organelos celulares",
                    "segments": [
                        {
                            "configuration": {
                                "type": "organelle_identification",
                                "organelles": [
                                    "nucleus",
                                    "mitochondria",
                                    "ribosome",
                                    "golgi",
                                    "er",
                                ],
                            }
                        },
                    ],
                },
                {
                    "level_number": 2,
                    "title": "Procesos Celulares",
                    "description": " mitosis y meiosis",
                    "goal": "Entender los procesos de división celular",
                    "segments": [
                        {
                            "configuration": {
                                "type": "mitosis",
                                "stages": [
                                    "profase",
                                    "metafase",
                                    "anafase",
                                    "telofase",
                                ],
                            }
                        },
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
            "download_link": "https://games.helloworld.edu/python-programming.zip",
            "levels": [
                {
                    "level_number": 1,
                    "title": "Variables y Tipos de Datos",
                    "description": "Introducción a Python",
                    "goal": "Crear variables y usar tipos de datos",
                    "segments": [
                        {"configuration": {"type": "variable_creation", "count": 10}},
                        {
                            "configuration": {
                                "type": "data_types",
                                "types": ["int", "float", "str", "bool"],
                            }
                        },
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
                        {"configuration": {"type": "for_loop", "range": (1, 10)}},
                        {"configuration": {"type": "while_loop", "exercises": 5}},
                    ],
                },
            ],
        },
    ]

    games = []
    for game_data in games_data:
        # Check if game exists
        query = select(Game).where(Game.title == game_data["title"])
        existing = (await db.execute(query)).scalars().first()

        if existing:
            print(f"Game '{game_data['title']}' already exists")
            games.append(existing)
            continue

        # Create game
        game = Game(
            title=game_data["title"],
            description=game_data["description"],
            creator=game_data["creator"],
            subject=game_data["subject"],
            publication_status=game_data["publication_status"],
            download_link=game_data["download_link"],
        )
        db.add(game)
        await db.flush()

        # Create levels
        for level_data in game_data.get("levels", []):
            level = Level(
                level_number=level_data["level_number"],
                title=level_data["title"],
                description=level_data["description"],
                goal=level_data["goal"],
                game_id=game.id,
            )
            db.add(level)
            await db.flush()

            # Create segments
            for segment_data in level_data.get("segments", []):
                segment = SegmentLevel(
                    level_number_id=level.id,
                    configuration=segment_data["configuration"],
                )
                db.add(segment)

        games.append(game)
        print(f"Seeded game: {game_data['title']}")

    return games


async def seed_game_instances(db: AsyncSession):
    """Seed game instances for students."""
    from src.users.domain.student import Student
    from src.game.domain.game import Game

    # Get some students and games
    students_query = select(Student).limit(10)
    students = (await db.execute(students_query)).scalars().all()

    games_query = select(Game).limit(3)
    games = (await db.execute(games_query)).scalars().all()

    if not students or not games:
        print("No students or games found for game instances")
        return []

    instances = []
    import random

    for i, student in enumerate(students):
        for j, game in enumerate(games):
            # Create some game instances
            for k in range(random.randint(1, 3)):
                started_at = datetime.now() - timedelta(days=random.randint(1, 30))

                # Random status
                status = random.choice(
                    [GameStatus.COMPLETED, GameStatus.ACTIVE, GameStatus.FAILED]
                )
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
                db.add(instance)
                instances.append(instance)

    print(f"Seeded {len(instances)} game instances")
    return instances
