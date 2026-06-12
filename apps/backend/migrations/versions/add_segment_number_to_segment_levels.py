"""add segment_number to segment_levels

Revision ID: add_segment_number_to_segment_levels
Revises: sync_sesh_timezone
Create Date: 2026-06-12 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_segment_number_to_segment_levels"
down_revision = "sync_sesh_timezone"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Step 1: Add column as nullable (allows backfill)
    op.add_column(
        "segment_levels",
        sa.Column("segment_number", sa.Integer(), nullable=True),
    )

    # Step 2: Backfill segment_number from configuration JSON (primary source of truth)
    # Each segment_level stores its segment_id in the configuration JSON blob.
    # This is the definitive ordering, not created_at (which may be identical for all segments).
    op.execute("""
        UPDATE segment_levels
        SET segment_number = (configuration->>'segment_id')::int
        WHERE configuration->>'segment_id' IS NOT NULL
          AND deleted_at IS NULL
    """)

    # Step 3: Backfill soft-deleted or config-less rows (assign sequential numbers)
    # For rows without configuration->segment_id, use row_number after existing ones
    op.execute("""
        UPDATE segment_levels
        SET segment_number = subquery.rn
        FROM (
            SELECT sl.id, sl.level_number_id,
                   COALESCE(max_active.seg_count, 0) + ROW_NUMBER() OVER (
                       PARTITION BY sl.level_number_id
                       ORDER BY sl.created_at ASC, sl.id ASC
                   ) AS rn
            FROM segment_levels sl
            LEFT JOIN (
                SELECT level_number_id, MAX(segment_number) AS seg_count
                FROM segment_levels
                WHERE segment_number IS NOT NULL
                GROUP BY level_number_id
            ) max_active ON max_active.level_number_id = sl.level_number_id
            WHERE sl.deleted_at IS NOT NULL
               OR (sl.configuration->>'segment_id') IS NULL
        ) AS subquery
        WHERE segment_levels.id = subquery.id
          AND segment_levels.segment_number IS NULL
    """)

    # Step 4: Make column non-nullable
    op.alter_column("segment_levels", "segment_number", nullable=False)

    # Step 5: Add unique constraint
    op.create_unique_constraint(
        "uq_segment_level_number",
        "segment_levels",
        ["level_number_id", "segment_number"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_segment_level_number", "segment_levels", type_="unique")
    op.drop_column("segment_levels", "segment_number")
