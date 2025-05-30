"""empty message

Revision ID: ba289ee11bd5
Revises: 78d08a8bd716
Create Date: 2025-04-29 13:26:26.931580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba289ee11bd5'
down_revision = '78d08a8bd716'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('refresh_token', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('refresh_token')

    # ### end Alembic commands ###
