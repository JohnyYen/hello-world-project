"""Add download_link column to games table

Revision ID: add_download_link_001
Revises: add_game_id_migration_001
Create Date: 2026-05-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_download_link_001'
down_revision = 'add_game_id_migration_001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'games',
        sa.Column('download_link', sa.String(500), nullable=False, server_default=''),
    )


def downgrade() -> None:
    op.drop_column('games', 'download_link')
