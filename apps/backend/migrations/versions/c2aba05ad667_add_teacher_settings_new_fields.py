"""add teacher_settings new fields

Revision ID: c2aba05ad667
Revises: add_xapi_statements
Create Date: 2026-03-22 18:05:36.206487

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "c2aba05ad667"
down_revision = "add_xapi_statements"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # TeacherSettings - Add new nullable columns for expanded settings
    op.add_column(
        "teacher_settings", sa.Column("auto_logout", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "teacher_settings",
        sa.Column("session_duration_minutes", sa.Integer(), nullable=True),
    )
    op.add_column(
        "teacher_settings", sa.Column("remember_login", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "teacher_settings",
        sa.Column("color_theme", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "teacher_settings", sa.Column("animations_enabled", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "teacher_settings",
        sa.Column("email_notifications", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "teacher_settings",
        sa.Column("date_format", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "teacher_settings", sa.Column("timezone", sa.String(length=50), nullable=True)
    )


def downgrade() -> None:
    # TeacherSettings - Remove new columns
    op.drop_column("teacher_settings", "timezone")
    op.drop_column("teacher_settings", "date_format")
    op.drop_column("teacher_settings", "email_notifications")
    op.drop_column("teacher_settings", "animations_enabled")
    op.drop_column("teacher_settings", "color_theme")
    op.drop_column("teacher_settings", "remember_login")
    op.drop_column("teacher_settings", "session_duration_minutes")
    op.drop_column("teacher_settings", "auto_logout")
