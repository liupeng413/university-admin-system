from app import db
from alembic import op
import sqlalchemy as sa

def upgrade():
    # 添加工号列
    op.add_column('user', sa.Column('employee_number', sa.Integer, nullable=True, default=0))
    
    # 更新现有记录的工号为0
    connection = op.get_bind()
    connection.execute('UPDATE user SET employee_number = 0 WHERE role = "teacher"')

def downgrade():
    # 删除工号列
    op.drop_column('user', 'employee_number') 