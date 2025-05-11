"""update user model

Revision ID: update_user_model_rev1
Revises: 
Create Date: 2024-03-20

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic
revision = 'update_user_model_rev1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 重命名表
    op.rename_table('user', 'users')
    
    # 添加新列
    op.add_column('users', sa.Column('education_level', sa.String(50)))
    op.add_column('users', sa.Column('highest_title', sa.String(50)))
    op.add_column('users', sa.Column('is_dual_teacher', sa.Boolean(), default=False))
    op.add_column('users', sa.Column('department', sa.String(100)))
    op.add_column('users', sa.Column('hire_date', sa.Date()))
    
    # 修改现有列的类型
    op.alter_column('users', 'birth_date',
                    existing_type=sa.String(50),
                    type_=sa.Date(),
                    postgresql_using="birth_date::date")
    
    # 删除不需要的列
    op.drop_column('users', 'ethnicity')
    op.drop_column('users', 'major')
    op.drop_column('users', 'teaching_group')

def downgrade():
    # 恢复删除的列
    op.add_column('users', sa.Column('teaching_group', sa.String(100)))
    op.add_column('users', sa.Column('major', sa.String(100)))
    op.add_column('users', sa.Column('ethnicity', sa.String(50)))
    
    # 恢复列类型
    op.alter_column('users', 'birth_date',
                    existing_type=sa.Date(),
                    type_=sa.String(50))
    
    # 删除新添加的列
    op.drop_column('users', 'hire_date')
    op.drop_column('users', 'department')
    op.drop_column('users', 'is_dual_teacher')
    op.drop_column('users', 'highest_title')
    op.drop_column('users', 'education_level')
    
    # 恢复表名
    op.rename_table('users', 'user') 