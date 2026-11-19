"""seed demo chatboxes data

Revision ID: d532f0c49db2
Revises:
Create Date: 2026-11-08 15:42:13.223669

Optional demo/testing chatboxes (with fake token history) for the dashboard.
Run after the baseline schema and seed data exist:
    alembic -c demo-alembic.ini upgrade head
"""
from typing import Sequence, Union

from alembic import context, op
import sqlalchemy as sa

from fixtures.test_fixtures.chatboxes import build_chatbox_rows


# revision identifiers, used by Alembic.
revision: str = 'd532f0c49db2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table(name: str) -> sa.Table:
    return sa.Table(name, sa.MetaData(), autoload_with=op.get_bind())


def _options() -> dict[str, int]:
    raw = context.get_x_argument(as_dictionary=True)
    options = {
        "users": int(raw.get("users", 1)),
        "days_back": int(raw.get("days-back", 180)),
        "chatboxes": int(raw.get("chatboxes", 6)),
        "messages": int(raw.get("messages", 10)),
    }

    if options["chatboxes"] > 0 and options["messages"] < 1:
        raise ValueError("messages must be >= 1 when chatboxes > 0")

    return options


def upgrade() -> None:
    """Upgrade schema."""
    options = _options()
    users_table = _table("users")
    user_ids = list(
        op.get_bind().execute(
            sa.select(users_table.c.id).limit(options["users"])
        ).scalars()
    )
    if not user_ids:
        raise RuntimeError(
            "No users found. Run `alembic -c initial-alembic.ini upgrade head` "
            "before seeding demo data."
        )

    rows = build_chatbox_rows(
        user_ids=user_ids,
        num_chatboxes=options["chatboxes"],
        num_messages=options["messages"],
        days_back=options["days_back"],
    )
    if rows:
        op.bulk_insert(_table("chatboxes"), rows)


def downgrade() -> None:
    """Downgrade schema."""
    # Demo data only; this clears the table entirely.
    op.execute(_table("chatboxes").delete())
