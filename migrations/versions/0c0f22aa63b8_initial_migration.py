"""Initial migration

Revision ID: 0c0f22aa63b8
Revises: 
Create Date: 2025-07-05 16:41:47.178272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c0f22aa63b8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cafes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=100), nullable=False),
    sa.Column('lokasi', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('kriteria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=100), nullable=False),
    sa.Column('bobot', sa.Float(), nullable=False),
    sa.Column('tipe', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ulasan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isi', sa.Text(), nullable=True),
    sa.Column('nilai', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cafe_id', sa.Integer(), nullable=False),
    sa.Column('kriteria_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cafe_id'], ['cafes.id'], ),
    sa.ForeignKeyConstraint(['kriteria_id'], ['kriteria.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ulasan')
    op.drop_table('users')
    op.drop_table('kriteria')
    op.drop_table('cafes')
    # ### end Alembic commands ###
