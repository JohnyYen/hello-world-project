"""add client_event_id to sync_events

Revision ID: abc123abc123
Revises: c2aba05ad667
Create Date: 2026-06-07 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "abc123abc123"
down_revision = "c2aba05ad667"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "sync_events",
        sa.Column("client_event_id", UUID(as_uuid=True), nullable=True),
    )
    op.create_index(
        "uq_sync_events_client_event_id",
        "sync_events",
        ["client_event_id"],
        unique=True,
        postgresql_where=sa.text("client_event_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_sync_events_client_event_id", table_name="sync_events")
    op.drop_column("sync_events", "client_event_id")
