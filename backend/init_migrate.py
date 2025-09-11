from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app, db

# 初始化 Flask-Migrate
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # 删除现有的数据库文件
        import os
        if os.path.exists('instance/database.db'):
            os.remove('instance/database.db')
            print("已删除旧的数据库文件")
        
        # 创建新的数据库
        db.create_all()
        print("已创建新的数据库表") 