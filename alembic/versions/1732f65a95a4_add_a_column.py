"""Add a column

Revision ID: 1732f65a95a4
Revises: 
Create Date: 2022-11-07 22:37:21.619818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1732f65a95a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Statistics', sa.Column('no_experience', sa.Integer,
                                          default=0))


def downgrade() -> None:
    op.drop_column('Statistics', 'no_experience')
