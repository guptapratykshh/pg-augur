"""Drop working_commits table

Revision ID: 38
Revises: 37
Create Date: 2026-01-10 09:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


#revision identifiers, used by Alembic.
revision = '38'
down_revision = '37'
branch_labels = None
depends_on = None


def upgrade():
    #attempt to drop from augur_data if it exists
    op.execute('DROP TABLE IF EXISTS augur_data.working_commits')
    #attempt to drop from augur_operations if it exists
    op.execute('DROP TABLE IF EXISTS augur_operations.working_commits')


def downgrade():
    #recreate in augur_data
    op.create_table('working_commits',
        sa.Column('repos_id', sa.Integer(), nullable=False),
        sa.Column('working_commit', sa.String(length=40), server_default=sa.text("'NULL'::character varying"), nullable=True),
        schema='augur_data',
    )
    
    #recreate in augur_operations
    op.create_table('working_commits',
        sa.Column('repos_id', sa.Integer(), nullable=False),
        sa.Column('working_commit', sa.String(length=40), server_default=sa.text("'NULL'::character varying"), nullable=True),
        schema='augur_operations',
        comment='For future use when we move all working tables to the augur_operations schema. '
    )
