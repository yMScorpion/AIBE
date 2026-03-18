# aibe/core/db/migrations/versions/001_initial_schema.py
"""Initial schema.

Revision ID: 001
Revises:
Create Date: 2026-03-17
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "agents",
        sa.Column("id", sa.String(50), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("tier", sa.Integer, nullable=False, index=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="initializing"),
        sa.Column("config", sa.JSON, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.String(50), primary_key=True),
        sa.Column("source_agent", sa.String(50), nullable=False, index=True),
        sa.Column("target_agent", sa.String(50), nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="submitted", index=True),
        sa.Column("priority", sa.Integer, nullable=False, server_default="5"),
        sa.Column("output_data", sa.JSON, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "meetings",
        sa.Column("id", sa.String(50), primary_key=True),
        sa.Column("topic", sa.String(255), nullable=False),
        sa.Column("participants", sa.JSON, nullable=False),
        sa.Column("meeting_type", sa.String(50), server_default="general"),
        sa.Column("max_rounds", sa.Integer, server_default="3"),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("rounds_completed", sa.Integer, server_default="0"),
        sa.Column("transcript", sa.JSON, nullable=True),
        sa.Column("result", sa.JSON, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "cost_records",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("agent_id", sa.String(50), nullable=False, index=True),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("task_type", sa.String(50), server_default="inference"),
        sa.Column("tokens_in", sa.Integer, server_default="0"),
        sa.Column("tokens_out", sa.Integer, server_default="0"),
        sa.Column("cost_usd", sa.Float, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
    )

    op.create_table(
        "secrets_audit",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("agent_id", sa.String(50), nullable=False, index=True),
        sa.Column("path", sa.String(500), nullable=False),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("secrets_audit")
    op.drop_table("cost_records")
    op.drop_table("meetings")
    op.drop_table("tasks")
    op.drop_table("agents")