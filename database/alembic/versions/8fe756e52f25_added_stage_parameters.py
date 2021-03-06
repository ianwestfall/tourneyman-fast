"""Added stage parameters

Revision ID: 8fe756e52f25
Revises: 9691ef1b1919
Create Date: 2021-03-13 21:07:00.725146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fe756e52f25'
down_revision = '9691ef1b1919'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stage', sa.Column('params', sa.JSON(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stage', 'params')
    # ### end Alembic commands ###
