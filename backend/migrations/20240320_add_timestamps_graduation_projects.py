"""添加时间戳字段到毕业设计表

Revision ID: 2
Create Date: 2024-03-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # 添加时间戳字段
    op.add_column('graduation_project',
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.add_column('graduation_project',
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade():
    # 删除时间戳字段
    op.drop_column('graduation_project', 'updated_at')
    op.drop_column('graduation_project', 'created_at') 