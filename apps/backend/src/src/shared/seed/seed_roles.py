from src.users.domain.role import Role
from sqlalchemy import select
from src.shared.infrastructure.session import AsyncSession

async def seed_role(db : AsyncSession):
    role = [
        {"role_name": "admin", "description": "Administrator with full access"},
        {"role_name": "professor", "description": "Professor with access to teaching resources" },
        {"role_name": "student", "description": "Student with access to learning materials" },
    ]

    for r in role:
        query = select(Role).where(Role.role_name == r["role_name"])
        existing_role = (await db.execute(query)).scalars().first()
        if not existing_role:
            new_role = Role(
                role_name = r["role_name"],
                description = r["description"]
            )
            db.add(new_role)
            print(f"Seeded role: {r['role_name']}")