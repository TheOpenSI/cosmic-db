"""pre-populate configurations data

Revision ID: 02307647b47e
Revises: 9dbf4c9febb6
Create Date: 2026-11-08 15:42:12.583668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from fixtures.data_fixtures import configurations


# revision identifiers, used by Alembic.
revision: str = '02307647b47e'
down_revision: Union[str, Sequence[str], None] = '9dbf4c9febb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        sa.Table(
            "configurations", sa.MetaData(), autoload_with=op.get_bind()
        ),
        configurations.configuration_rows()
    )


def downgrade() -> None:
    """Downgrade schema."""
    configurations_table = sa.Table(
        "configurations", sa.MetaData(), autoload_with=op.get_bind()
    )
    op.execute(
        configurations_table.delete().where(
            configurations_table.c.name == configurations.CONFIG_NAME
        )
    )
