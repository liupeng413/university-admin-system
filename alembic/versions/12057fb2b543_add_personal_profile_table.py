"""add personal_profile table

Revision ID: 12057fb2b543
Revises: 
Create Date: 2025-04-26 16:45:30.023052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12057fb2b543'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 只创建personal_profile表
    op.create_table(
        'personal_profile',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('name', sa.String(length=80)),
        sa.Column('employee_number', sa.String(length=20)),
        sa.Column('gender', sa.String(length=10)),
        sa.Column('ethnicity', sa.String(length=50)),
        sa.Column('birth_date', sa.Date()),
        sa.Column('id_number', sa.String(length=18)),
        sa.Column('political_status', sa.String(length=50)),
        sa.Column('party_branch', sa.String(length=100)),
        sa.Column('hometown', sa.String(length=100)),
        sa.Column('phone', sa.String(length=20)),
        sa.Column('email', sa.String(length=120)),
        sa.Column('address', sa.String(length=200)),
        sa.Column('education_level', sa.String(length=50)),
        sa.Column('degree', sa.String(length=50)),
        sa.Column('education_date', sa.Date()),
        sa.Column('degree_date', sa.Date()),
        sa.Column('bachelor_school', sa.String(length=100)),
        sa.Column('master_school', sa.String(length=100)),
        sa.Column('phd_school', sa.String(length=100)),
        sa.Column('research_direction', sa.String(length=200)),
        sa.Column('work_start_date', sa.Date()),
        sa.Column('career_start_date', sa.Date()),
        sa.Column('highest_title', sa.String(length=50)),
        sa.Column('highest_title_date', sa.Date()),
        sa.Column('position', sa.String(length=50)),
        sa.Column('subject', sa.String(length=50)),
        sa.Column('department', sa.String(length=100)),
        sa.Column('photo_path', sa.String(length=200)),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('personal_profile')
