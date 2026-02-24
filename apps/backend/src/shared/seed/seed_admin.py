from src.users.domain.user import User
from src.shared.infrastructure.session import AsyncSession
from sqlalchemy import select


async def seed_admin(db: AsyncSession):
    """Seed the admin user if it doesn't exist."""
    # Verificar si el usuario admin ya existe
    query = select(User).where(User.username == "superadmin")
    admin = (await db.execute(query)).scalars().first()
    if admin:
        print("Admin user 'superadmin' already exists")
        return

    # Buscar el rol de admin por nombre (más robusto que usar ID hardcodeado)
    from src.users.domain.role import Role

    role_query = select(Role).where(Role.role_name == "admin")
    admin_role = (await db.execute(role_query)).scalars().first()

    if not admin_role:
        print("Warning: Admin role not found. Run seed_roles first.")
        return

    print("Seeding admin user...")
    admin = User(
        username="superadmin",
        name="Admin",
        email="admin@example.com",
        is_active=True,
        hashed_password="$2b$12$h8b3DBzDYqlsA/HBVexAuukd0.KEEYYp3pvRTVOJ4pRhymA5xM73O",  # "adminpass123" hasheado
        role_id=admin_role.id,
    )
    db.add(admin)
    print("Seeded admin user: superadmin")
