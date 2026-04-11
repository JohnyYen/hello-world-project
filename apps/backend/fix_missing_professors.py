#!/usr/bin/env python3
"""
Script para corregir usuarios professors que no tienen registro en la tabla professors.
Este script busca todos los usuarios con rol 'professor' y crea el registro correspondiente
si no existe.
"""

import asyncio
import sys
from sqlalchemy import create_engine, select, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import uuid


async def fix_missing_professors(database_url: str):
    """
    Busca todos los usuarios con rol 'professor' y crea el registro en professors si no existe.
    """
    # Crear motor asíncrono
    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Buscar usuarios con rol professor que no tienen registro en professors
        query = text("""
            SELECT u.id, u.username, u.email
            FROM users u
            JOIN roles r ON u.role_id = r.id
            LEFT JOIN professors p ON u.id = p.user_id
            WHERE r.role_name = 'professor'
            AND p.id IS NULL
            AND u.deleted_at IS NULL
        """)

        result = await session.execute(query)
        missing_professors = result.fetchall()

        if not missing_professors:
            print("✅ No se encontraron usuarios professors sin registro.")
            return

        print(f"🔍 Se encontraron {len(missing_professors)} usuarios professors sin registro:")
        for row in missing_professors:
            print(f"  - {row.username} ({row.email}) [ID: {row.id}]")

        # Crear registros de professors faltantes
        print("\n🛠️  Creando registros de professors...")

        insert_query = text("""
            INSERT INTO professors (id, user_id, department, contact_phone, created_at, updated_at, is_deleted)
            VALUES (:id, :user_id, 'General', NULL, NOW(), NOW(), FALSE)
        """)

        created_count = 0
        for user_row in missing_professors:
            try:
                professor_id = str(uuid.uuid4())
                await session.execute(insert_query, {
                    "id": professor_id,
                    "user_id": str(user_row.id),
                })
                created_count += 1
                print(f"  ✅ Creado registro para {user_row.username}")
            except Exception as e:
                print(f"  ❌ Error al crear registro para {user_row.username}: {e}")

        # Commit de los cambios
        await session.commit()
        print(f"\n✅ Se crearon {created_count} registros de professors exitosamente.")

    await engine.dispose()


if __name__ == "__main__":
    # URL de la base de datos (ajustar según configuración)
    # Formato: postgresql+asyncpg://user:password@host:port/dbname
    if len(sys.argv) > 1:
        DATABASE_URL = sys.argv[1]
    else:
        # URL para ejecución dentro del contenedor Docker
        DATABASE_URL = "postgresql+asyncpg://hwp_user:hwp_password@postgresql_db:5432/hwp_db"

    print("Script para corregir usuarios professors sin registro")
    print("=" * 50)
    print(f"Base de datos: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else 'local'}\n")

    try:
        asyncio.run(fix_missing_professors(DATABASE_URL))
    except Exception as e:
        print(f"❌ Error ejecutando el script: {e}", file=sys.stderr)
        sys.exit(1)
