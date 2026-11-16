"""pre-populate services data

Revision ID: 9dbf4c9febb6
Revises: acbcfab32793
Create Date: 2026-11-08 15:42:11.927743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from fixtures.data_fixtures import services


# revision identifiers, used by Alembic.
revision: str = '9dbf4c9febb6'
down_revision: Union[str, Sequence[str], None] = 'acbcfab32793'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        sa.Table("services", sa.MetaData(), autoload_with=op.get_bind()),
        services.service_rows()
    )


def downgrade() -> None:
    """Downgrade schema."""
    services_table = sa.Table(
        "services", sa.MetaData(), autoload_with=op.get_bind()
    )
    op.execute(
        services_table.delete().where(
            services_table.c.name.in_(services.SERVICE_NAMES)
        )
    )
