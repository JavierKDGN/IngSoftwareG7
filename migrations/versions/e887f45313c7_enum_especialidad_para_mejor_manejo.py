"""Enum especialidad para mejor manejo

Revision ID: e887f45313c7
Revises: b609f1145484
Create Date: 2024-11-17 14:40:31.356513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e887f45313c7'
down_revision = 'b609f1145484'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('medico', schema=None) as batch_op:
        batch_op.alter_column('especialidad',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Enum('CARDIOLOGIA', 'PEDIATRIA', 'DERMATOLOGIA', 'GINECOLOGIA', 'NEUROLOGIA', 'OTORRINOLARINGOLOGIA', 'PSIQUIATRIA', 'TRAUMATOLOGIA', name='especialidad'),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('medico', schema=None) as batch_op:
        batch_op.alter_column('especialidad',
               existing_type=sa.Enum('CARDIOLOGIA', 'PEDIATRIA', 'DERMATOLOGIA', 'GINECOLOGIA', 'NEUROLOGIA', 'OTORRINOLARINGOLOGIA', 'PSIQUIATRIA', 'TRAUMATOLOGIA', name='especialidad'),
               type_=sa.VARCHAR(length=64),
               existing_nullable=False)

    # ### end Alembic commands ###
