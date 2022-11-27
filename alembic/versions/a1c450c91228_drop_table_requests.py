"""drop table Requests

Revision ID: a1c450c91228
Revises: ab5f2845ce10
Create Date: 2022-11-07 22:57:04.131136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1c450c91228'
down_revision = 'ab5f2845ce10'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('Requests')


def downgrade() -> None:
    pass
