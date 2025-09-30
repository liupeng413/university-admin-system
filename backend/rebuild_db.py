from app import app, db
from models import User
import os

def rebuild_database():
    with app.app_context():
        # 确保instance目录存在
        os.makedirs('instance', exist_ok=True)
        
        # 删除所有表
        db.drop_all()
        # 创建所有表
        db.create_all()
        print("数据库已重建完成！")

if __name__ == "__main__":
    rebuild_database() 