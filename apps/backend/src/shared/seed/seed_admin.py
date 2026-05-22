from src.users.domain.user import User
from src.shared.infrastructure.session import AsyncSession
from src.shared.infrastructure.config import settings
from src.auth.infrastructure.security import get_password_hash
from sqlalchemy import select


async def seed_admin(db: AsyncSession):
    """Seed the admin user if it doesn't exist.
    
    Uses ADMIN_USERNAME and ADMIN_PASSWORD from environment variables.
    """
    # Get admin credentials from environment
    admin_username = settings.ADMIN_USERNAME
    admin_password = settings.ADMIN_PASSWORD
    
    # Verify if admin user already exists
    query = select(User).where(User.username == admin_username)
    admin = (await db.execute(query)).scalars().first()
    if admin:
        print(f"Admin user '{admin_username}' already exists")
        return

    # Find admin role by name
    from src.users.domain.role import Role

    role_query = select(Role).where(Role.role_name == "admin")
    admin_role = (await db.execute(role_query)).scalars().first()

    if not admin_role:
        print("Warning: Admin role not found. Run seed_roles first.")
        return

    print(f"Seeding admin user: {admin_username}...")
    
    # Hash password from environment variable
    hashed_password = get_password_hash(admin_password)
    
    admin = User(
        username=admin_username,
        name="Admin",
        email="admin@example.com",
        is_active=True,
        hashed_password=hashed_password,
        role_id=admin_role.id,
    )
    db.add(admin)
    print(f"Seeded admin user: {admin_username}")
