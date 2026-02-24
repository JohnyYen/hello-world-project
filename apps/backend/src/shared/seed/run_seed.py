from src.shared.infrastructure.session import SessionLocal
from src.shared.seed.seed_roles import seed_role
from src.shared.seed.seed_admin import seed_admin


async def run_all_seeds():
    db = SessionLocal()
    try:
        print("Seeding database...")
        await seed_role(db)
        await seed_admin(db)
        await db.commit()
        print("Seeding completed.")
    except Exception as e:
        await db.rollback()
        print(f"Seeding failed: {e}")
    finally:
        await db.close()


if __name__ == "__main__":
    run_all_seeds()
