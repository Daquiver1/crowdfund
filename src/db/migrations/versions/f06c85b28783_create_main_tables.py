"""create main tables

Revision ID: f06c85b28783
Revises:
Create Date: 2024-01-26 06:11:04.247982

"""

from typing import Optional, Sequence, Tuple, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f06c85b28783"
down_revision: Optional[str] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_updated_at_trigger() -> None:
    """Update timestamp trigger."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    """Create timestamp in DB."""
    return (
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=func.now(),
            index=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=func.now(),
            index=True,
        ),
    )


def is_deleted() -> sa.Column:
    """Create is_deleted column."""
    return sa.Column(
        "is_deleted", sa.Boolean, nullable=False, server_default=sa.false(), index=True
    )


def create_users_table() -> None:
    """Create users table for authentication."""
    op.create_table(
        "users",
        sa.Column(
            "user_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
        ),
        sa.Column("first_name", sa.String(100), nullable=True),
        sa.Column("last_name", sa.String(100), nullable=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("username", sa.String(50), nullable=False, unique=True, index=True),
        *timestamps(),
        is_deleted(),
    )
    op.execute(
        """
        CREATE TRIGGER update_users_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def create_projects_table() -> None:
    """Create projects table."""
    op.create_table(
        "projects",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "owner_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.user_id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("goal_amount", sa.Integer(), nullable=False),
        sa.Column("deadline", sa.TIMESTAMP(timezone=True), nullable=False, index=True),
        *timestamps(),
        is_deleted(),
    )
    op.create_check_constraint(
        "chk_projects_goal_amount_non_negative", "projects", "goal_amount >= 0"
    )
    op.execute(
        """
        CREATE TRIGGER update_projects_modtime
            BEFORE UPDATE
            ON projects
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def create_contributions_table() -> None:
    """Create contributions table."""
    op.create_table(
        "contributions",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "project_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "contributor_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.user_id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("amount", sa.Integer(), nullable=False),
        *timestamps(),
        is_deleted(),
    )
    op.create_check_constraint(
        "chk_contributions_amount_non_negative", "contributions", "amount >= 0"
    )
    op.execute(
        """
        CREATE TRIGGER update_contributions_modtime
            BEFORE UPDATE
            ON contributions
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def upgrade() -> None:
    """Upgrade DB."""
    create_updated_at_trigger()
    create_users_table()
    create_projects_table()
    create_contributions_table()


def downgrade() -> None:
    """Downgrade DB."""
    tables = [
        "contributions",
        "projects",
        "users",
    ]

    for table in tables:
        op.execute(f"DROP TABLE IF EXISTS {table}")

    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE")
