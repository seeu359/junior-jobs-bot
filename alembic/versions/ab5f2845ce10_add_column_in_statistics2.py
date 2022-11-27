"""add column in statistics2

Revision ID: ab5f2845ce10
Revises: bf472de67613
Create Date: 2022-11-07 22:54:16.617990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab5f2845ce10'
down_revision = 'bf472de67613'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Statistics', sa.Column('no_experience', sa.Integer,
                                          default=0))


def downgrade() -> None:
    op.drop_column('Statistics', 'no_experience')

