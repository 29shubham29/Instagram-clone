"""followers

Revision ID: 657d6afebef1
Revises: d9de82741da0
Create Date: 2019-09-24 14:11:00.157566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '657d6afebef1'
down_revision = 'd9de82741da0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###