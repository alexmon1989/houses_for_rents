"""empty message

Revision ID: fcc383c586dd
Revises: 937a3d4d4ccf
Create Date: 2016-10-23 18:22:33.503572

"""

# revision identifiers, used by Alembic.
revision = 'fcc383c586dd'
down_revision = '937a3d4d4ccf'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('listings', 'agent_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('listings', 'manager_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('listings', 'manager_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('listings', 'agent_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    ### end Alembic commands ###
