"""pre-populate users data

Revision ID: acbcfab32793
Revises: de01680619d0
Create Date: 2026-11-08 15:42:11.260575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from fixtures.data_fixtures import users


# revision identifiers, used by Alembic.
revision: str = 'acbcfab32793'
down_revision: Union[str, Sequence[str], None] = 'de01680619d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table(name: str) -> sa.Table:
    return sa.Table(name, sa.MetaData(), autoload_with=op.get_bind())


def upgrade() -> None:
    """Upgrade schema."""
    roles_table = _table("roles")
    role_ids = {
        name: role_id
        for name, role_id in op.get_bind().execute(
            sa.select(roles_table.c.name, roles_table.c.id)
        )
    }
    op.bulk_insert(_table("users"), users.user_rows(role_ids))


def downgrade() -> None:
    """Downgrade schema."""
    users_table = _table("users")
    op.execute(
        users_table.delete().where(users_table.c.email == users.ADMIN_EMAIL)
    )
