"""User Confirm column

Revision ID: 28eb1ed520b5
Revises: 91c91427881b
Create Date: 2019-10-13 15:12:27.160706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28eb1ed520b5'
down_revision = '91c91427881b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'confirmed')
    # ### end Alembic commands ###
