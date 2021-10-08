"""Initial migration. Create employee model.

Revision ID: efdfe4de1d23
Revises: 
Create Date: 2021-10-05 11:17:22.082416

"""
from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efdfe4de1d23'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """alembic -x data=true upgrade head"""
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()

def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()

def schema_upgrades():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usr_employee',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_usr_employee_id'), 'usr_employee', ['id'], unique=False)
    # ### end Alembic commands ###

def schema_downgrades():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_usr_employee_id'), table_name='usr_employee')
    op.drop_table('usr_employee')
    # ### end Alembic commands ###

def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass