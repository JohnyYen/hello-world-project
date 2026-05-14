from src.users.domain.notification import Notification
from src.shared.infrastructure.session import AsyncSession
from sqlalchemy import select
import random


async def seed_notifications(db: AsyncSession):
    """Seed notifications for users."""
    from src.users.domain.user import User

    users_query = select(User).limit(30)
    users = (await db.execute(users_query)).scalars().all()

    if not users:
        print("No users found for notifications")
        return []

    notification_templates = [
        {
            "type": "game_invite",
            "title": "Nueva invitación de juego",
            "message": "Has sido invitado a jugar 'Matemáticas Básicas'",
        },
        {
            "type": "course_enrollment",
            "title": "Matrícula confirmada",
            "message": "Tu matrícula en 'Introducción a la Programación' ha sido confirmada",
        },
        {
            "type": "feedback_received",
            "title": "Nuevo feedback recibido",
            "message": "El profesor ha enviado feedback sobre tu último juego",
        },
        {
            "type": "progress_update",
            "title": "Actualización de progreso",
            "message": "Has completado el nivel 2 de 'Física Fundamental'",
        },
        {
            "type": "achievement",
            "title": "¡Logro desbloqueado!",
            "message": "Has completado 10 juegos correctamente",
        },
        {
            "type": "system",
            "title": "Mantenimiento del sistema",
            "message": "El sistema estará en mantenimiento el domingo de 2am a 6am",
        },
        {
            "type": "reminder",
            "title": "Recordatorio de tarea",
            "message": "Tienes una tarea pendiente en 'Química Introductoria'",
        },
        {
            "type": "announcement",
            "title": "Nuevo contenido disponible",
            "message": "Se ha añadido un nuevo nivel al juego 'Programación con Python'",
        },
    ]

    notifications = []
    for user in users:
        # Create 2-5 notifications per user
        num_notifications = random.randint(2, 5)

        for _ in range(num_notifications):
            template = random.choice(notification_templates)

            notification = Notification(
                title=template["title"],
                message=template["message"],
                is_read=random.choice([True, False, False]),  # 1/3 probability of read
                notification_type=template["type"],
                user_id=user.id,
                entity_type=random.choice(["game", "course", "level", None]),
                entity_id=None,
            )
            db.add(notification)
            notifications.append(notification)

    print(f"Seeded {len(notifications)} notifications")
    return notifications
