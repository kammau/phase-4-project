"""changed id's in association table

Revision ID: 9a1baad73caa
Revises: d4d4250fa46b
Create Date: 2023-10-02 14:14:28.492792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a1baad73caa'
down_revision = 'd4d4250fa46b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('common_name', sa.String(), nullable=True),
    sa.Column('scientific_name', sa.String(), nullable=True),
    sa.Column('growing_level', sa.Integer(), nullable=True),
    sa.Column('img', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('genre', sa.String(), nullable=True),
    sa.Column('img', sa.String(), nullable=True),
    sa.Column('user', sa.String(), nullable=True),
    sa.Column('plant', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['plant'], ['plants.common_name'], name=op.f('fk_posts_plant_plants')),
    sa.ForeignKeyConstraint(['user'], ['users.username'], name=op.f('fk_posts_user_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_plant',
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('plant_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['plant_id'], ['plants.common_name'], name=op.f('fk_user_plant_plant_id_plants')),
    sa.ForeignKeyConstraint(['user_id'], ['users.username'], name=op.f('fk_user_plant_user_id_users'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_plant')
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_table('plants')
    # ### end Alembic commands ###
