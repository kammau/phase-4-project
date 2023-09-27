"""posts serial rules

Revision ID: 0ba40e2e6910
Revises: 7eb58a03f703
Create Date: 2023-09-26 14:36:06.535798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ba40e2e6910'
down_revision = '7eb58a03f703'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_plant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plant_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_user_plant_plant_plants', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_user_plant_plant_id_plants'), 'plants', ['plant_id'], ['id'])
        batch_op.drop_column('plant')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_plant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plant', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_user_plant_plant_id_plants'), type_='foreignkey')
        batch_op.create_foreign_key('fk_user_plant_plant_plants', 'plants', ['plant'], ['id'])
        batch_op.drop_column('plant_id')

    # ### end Alembic commands ###