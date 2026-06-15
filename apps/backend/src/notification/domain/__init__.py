"""
Notification domain models.

The canonical Notification model lives in src.users.domain.notification
to avoid circular imports with the User model relationship.
This module re-exports it for clean imports from the notification package.
"""

from src.users.domain.notification import Notification

__all__ = [
    "Notification",
]
