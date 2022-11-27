"""create users table

Revision ID: 8d619ad6e3d2
Revises: 1732f65a95a4
Create Date: 2022-11-07 22:39:26.736888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d619ad6e3d2'
down_revision = '1732f65a95a4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'Users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('telegram_id', sa.Integer, nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table('Users')
