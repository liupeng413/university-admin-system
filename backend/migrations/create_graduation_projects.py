"""创建毕业设计表

Revision ID: 1
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # 创建毕业设计表
    op.create_table(
        'graduation_project',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('graduation_year', sa.Integer(), nullable=False),
        sa.Column('student_name', sa.String(255), nullable=False),
        sa.Column('student_id', sa.String(255), nullable=False),
        sa.Column('major', sa.String(255), nullable=False),
        sa.Column('class_name', sa.String(255), nullable=False),
        sa.Column('project_title', sa.String(255), nullable=False),
        sa.Column('project_type', sa.String(255), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('grade', sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(['teacher_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # 删除毕业设计表
    op.drop_table('graduation_project') 