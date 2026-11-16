"""pre-populate roles data

Revision ID: de01680619d0
Revises: 8289aeeca3c1
Create Date: 2026-11-08 15:42:10.596638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from fixtures.data_fixtures import roles


# revision identifiers, used by Alembic.
revision: str = 'de01680619d0'
down_revision: Union[str, Sequence[str], None] = '8289aeeca3c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        sa.Table("roles", sa.MetaData(), autoload_with=op.get_bind()),
        roles.role_rows()
    )


def downgrade() -> None:
    """Downgrade schema."""
    roles_table = sa.Table(
        "roles", sa.MetaData(), autoload_with=op.get_bind()
    )
    op.execute(
        roles_table.delete().where(roles_table.c.name.in_(roles.ROLE_NAMES))
    )
