import os
from app import db, User, app
from werkzeug.security import generate_password_hash
from datetime import datetime, date

def init_db():
    """初始化数据库"""
    # 确保实例目录存在
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    # 创建所有表（如果不存在）
    with app.app_context():
        db.create_all()
        print("数据库表已创建/更新")
    
    # 创建管理员账号
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            name='系统管理员',
            major='信息技术',
            title='管理员',
            gender='男',
            ethnicity='汉族',
            birth_date=date(1980, 1, 1),
            bachelor_school='示例大学',
            master_school='示例大学',
            phd_school=None,
            research_direction='系统管理与维护',
            work_start_date=date(2000, 1, 1)
        )
        db.session.add(admin)
        db.session.commit()
        print('管理员账号创建成功！')
    
    if not User.query.filter_by(username='teacher').first():
        teacher = User(
            username='teacher',
            password_hash=generate_password_hash('teacher123'),
            role='teacher',
            name='张老师',
            major='计算机科学与技术',
            title='副教授',
            gender='男',
            ethnicity='汉族',
            birth_date=date(1985, 6, 15),
            bachelor_school='北京大学',
            master_school='清华大学',
            phd_school='中国科学院',
            research_direction='人工智能与机器学习',
            work_start_date=date(2010, 7, 1)
        )
        db.session.add(teacher)
    
    if not User.query.filter_by(username='user').first():
        user = User(
            username='user',
            password_hash=generate_password_hash('user123'),
            role='user',
            name='李老师',
            major='应用数学',
            title='讲师',
            gender='女',
            ethnicity='汉族',
            birth_date=date(1990, 3, 20),
            bachelor_school='复旦大学',
            master_school='上海交通大学',
            phd_school=None,
            research_direction='应用数学与统计',
            work_start_date=date(2015, 9, 1)
        )
        db.session.add(user)
    
    # 更新指定用户的权限
    zhangyanpeng = User.query.filter_by(username='zhangyanpeng').first()
    if zhangyanpeng:
        zhangyanpeng.role = 'admin'
        
    wangpeng = User.query.filter_by(username='wangpeng').first()
    if wangpeng:
        wangpeng.role = 'admin'
    
    db.session.commit()

if __name__ == '__main__':
    init_db()
    print('数据库初始化完成！') 