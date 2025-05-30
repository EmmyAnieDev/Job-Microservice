"""initial migration

Revision ID: cf9124686faa
Revises: 
Create Date: 2025-05-25 00:00:50.793934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf9124686faa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_applications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(length=255), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('company', sa.String(length=255), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('salary', sa.Float(), nullable=True),
    sa.Column('applied_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_applications_id'), 'job_applications', ['id'], unique=False)
    op.create_index(op.f('ix_job_applications_job_id'), 'job_applications', ['job_id'], unique=False)
    op.create_index(op.f('ix_job_applications_user_email'), 'job_applications', ['user_email'], unique=False)
    op.create_index(op.f('ix_job_applications_user_id'), 'job_applications', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_job_applications_user_id'), table_name='job_applications')
    op.drop_index(op.f('ix_job_applications_user_email'), table_name='job_applications')
    op.drop_index(op.f('ix_job_applications_job_id'), table_name='job_applications')
    op.drop_index(op.f('ix_job_applications_id'), table_name='job_applications')
    op.drop_table('job_applications')
    # ### end Alembic commands ###
