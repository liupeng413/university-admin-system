from app import app, db
from flask_migrate import Migrate, upgrade
import os

# 初始化 Flask-Migrate
migrate = Migrate(app, db)

def run_migrations():
    """运行所有待执行的数据库迁移"""
    with app.app_context():
        # 确保migrations目录存在
        if not os.path.exists('migrations'):
            os.makedirs('migrations')
        
        # 运行迁移
        upgrade()
        print("数据库迁移完成！")

if __name__ == '__main__':
    run_migrations() 