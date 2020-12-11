"""empty message

Revision ID: b9e564ce4f2c
Revises: 
Create Date: 2020-12-11 14:35:33.560781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9e564ce4f2c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('AnnouncementType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('firstname', sa.String(length=64), nullable=False),
    sa.Column('lastname', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('location', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['location'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id', 'username')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('announcement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('authorid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('pub_date', sa.String(length=11), nullable=False),
    sa.Column('location', sa.Integer(), nullable=False),
    sa.Column('announcement_type', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['announcement_type'], ['AnnouncementType.id'], ),
    sa.ForeignKeyConstraint(['authorid'], ['user.id'], ),
    sa.ForeignKeyConstraint(['location'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('announcement')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('location')
    op.drop_table('AnnouncementType')
    # ### end Alembic commands ###