"""Add game_id to courses and course_id to game_instances

Game Publisher: phase 1 — nullable FKs, no constraint enforcement yet.

Revision ID: add_game_id_migration_001
Revises: add_soft_delete_courses
Create Date: 2026-05-20

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_game_id_migration_001'
down_revision = 'add_soft_delete_courses'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add game_id nullable FK on courses, course_id nullable FK on game_instances."""
    # Phase 1: both columns are nullable — no application-level constraint yet.
    op.add_column('courses', sa.Column('game_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'courses_game_id_fkey',
        'courses', 'games',
        ['game_id'], ['id'],
        ondelete='SET NULL',
    )

    op.add_column('game_instances', sa.Column('course_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'game_instances_course_id_fkey',
        'game_instances', 'courses',
        ['course_id'], ['id'],
        ondelete='SET NULL',
    )


def downgrade() -> None:
    """Remove course_id from game_instances, game_id from courses."""
    op.drop_constraint('game_instances_course_id_fkey', 'game_instances', type_='foreignkey')
    op.drop_column('game_instances', 'course_id')

    op.drop_constraint('courses_game_id_fkey', 'courses', type_='foreignkey')
    op.drop_column('courses', 'game_id')
