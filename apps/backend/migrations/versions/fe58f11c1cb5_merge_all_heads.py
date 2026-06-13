"""merge all heads

Revision ID: fe58f11c1cb5
Revises: 5f852d7aed6f, add_download_link_001, add_feedback_game_fields, add_segment_number_to_segment_levels
Create Date: 2026-06-12 14:06:45.411455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe58f11c1cb5'
down_revision = ('5f852d7aed6f', 'add_download_link_001', 'add_feedback_game_fields', 'add_segment_number_to_segment_levels')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
