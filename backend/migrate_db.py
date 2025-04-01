from app import create_app, db
from app.models import User

app = create_app()

def migrate_db():
    with app.app_context():
        # 添加工号列
        db.engine.execute('ALTER TABLE user ADD COLUMN employee_number INTEGER DEFAULT 0')
        
        # 更新所有教师的工号为0
        db.engine.execute('UPDATE user SET employee_number = 0 WHERE role = "teacher"')
        
        print("数据库迁移完成！")

if __name__ == '__main__':
    migrate_db() 