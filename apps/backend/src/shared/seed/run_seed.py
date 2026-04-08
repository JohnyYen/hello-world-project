from src.shared.infrastructure.session import SessionLocal
from src.shared.seed.seed_roles import seed_role
from src.shared.seed.seed_admin import seed_admin
from src.shared.seed.seed_users import seed_all_users
from src.shared.seed.seed_lms_credentials import seed_lms_credentials
from src.shared.seed.seed_games import seed_games, seed_game_instances
from src.shared.seed.seed_courses import seed_courses, seed_enrollments
from src.shared.seed.seed_statistics import (
    seed_metric_types,
    seed_feedbacks,
    seed_progress,
    seed_xapi_statements,
)
from src.shared.seed.seed_notifications import seed_notifications


async def run_all_seeds():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("Starting database seeding...")
        print("=" * 50)

        # Phase 1: Core data (roles and admin)
        print("\n[Phase 1] Seeding roles and admin...")
        await seed_role(db)
        await seed_admin(db)

        # Phase 2: Users (professors and students)
        print("\n[Phase 2] Seeding users...")
        professors, students = await seed_all_users(db)

        # Phase 3: LMS credentials
        print("\n[Phase 3] Seeding LMS credentials...")
        await seed_lms_credentials(db)

        # Phase 4: Games with levels and segments
        print("\n[Phase 4] Seeding games...")
        games = await seed_games(db)

        # Phase 5: Game instances
        print("\n[Phase 5] Seeding game instances...")
        await seed_game_instances(db)

        # Phase 6: Courses
        print("\n[Phase 6] Seeding courses...")
        courses = await seed_courses(db)

        # Phase 7: Course enrollments
        print("\n[Phase 7] Seeding course enrollments...")
        await seed_enrollments(db)

        # Phase 8: Statistics (metric types, feedbacks, progress, xAPI)
        print("\n[Phase 8] Seeding statistics...")
        await seed_metric_types(db)
        await seed_feedbacks(db)
        await seed_progress(db)
        await seed_xapi_statements(db)

        # Phase 9: Notifications
        print("\n[Phase 9] Seeding notifications...")
        await seed_notifications(db)

        # Commit all changes
        await db.commit()

        print("\n" + "=" * 50)
        print("Seeding completed successfully!")
        print("=" * 50)

    except Exception as e:
        await db.rollback()
        print(f"\nSeeding failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        await db.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_all_seeds())
