"""Add missing columns to teacher_internship table

Revision ID: update_teacher_internship
Revises: 
Create Date: 2024-03-21

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_teacher_internship'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 添加缺失的列到teacher_internship表
    with op.batch_alter_table('teacher_internship') as batch_op:
        batch_op.add_column(sa.Column('college', sa.String(100), nullable=True))
        batch_op.add_column(sa.Column('major', sa.String(100), nullable=True))
        batch_op.add_column(sa.Column('major_type', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('class_name', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('student_id', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('student_name', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(10), nullable=True))
        batch_op.add_column(sa.Column('student_phone', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('internship_score', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('is_excellent', sa.Boolean, nullable=True))
        batch_op.add_column(sa.Column('internship_type', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('start_date', sa.Date, nullable=True))
        batch_op.add_column(sa.Column('end_date', sa.Date, nullable=True))
        batch_op.add_column(sa.Column('internship_company', sa.String(200), nullable=True))
        batch_op.add_column(sa.Column('province', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(200), nullable=True))
        batch_op.add_column(sa.Column('base_type', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('external_teacher_name', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('external_teacher_title', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('external_teacher_phone', sa.String(20), nullable=True))

def downgrade():
    # 删除添加的列
    with op.batch_alter_table('teacher_internship') as batch_op:
        batch_op.drop_column('college')
        batch_op.drop_column('major')
        batch_op.drop_column('major_type')
        batch_op.drop_column('class_name')
        batch_op.drop_column('student_id')
        batch_op.drop_column('student_name')
        batch_op.drop_column('gender')
        batch_op.drop_column('student_phone')
        batch_op.drop_column('internship_score')
        batch_op.drop_column('is_excellent')
        batch_op.drop_column('internship_type')
        batch_op.drop_column('start_date')
        batch_op.drop_column('end_date')
        batch_op.drop_column('internship_company')
        batch_op.drop_column('province')
        batch_op.drop_column('city')
        batch_op.drop_column('address')
        batch_op.drop_column('base_type')
        batch_op.drop_column('external_teacher_name')
        batch_op.drop_column('external_teacher_title')
        batch_op.drop_column('external_teacher_phone') 