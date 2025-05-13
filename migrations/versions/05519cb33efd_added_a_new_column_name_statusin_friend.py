"""added a new column name statusin_friend

Revision ID: 05519cb33efd
Revises: 
Create Date: 2023-05-19 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05519cb33efd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('friend', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('status', sa.String(), nullable=False, server_default='PENDING')
        )


def downgrade():
    with op.batch_alter_table('friend', schema=None) as batch_op:
        batch_op.drop_column('status')