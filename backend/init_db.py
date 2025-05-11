import os
from app import app
from models import (
    db, User, GraduationProject, TeacherCourse, Internship,
    TeachingProject, EvaluationProject, ResearchPaper,
    InnovationProject, Competition, CollegeEvent,
    FiveOneMentor, File, FiveOneProject
)
from datetime import datetime
import pandas as pd

def init_db():
    """初始化数据库"""
    print("开始初始化数据库...")
    
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(current_dir, '..', 'instance')
    
    # 确保实例目录存在
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"创建实例目录成功：{instance_dir}")
    else:
        print(f"实例目录已存在：{instance_dir}")
    
    # 删除现有的数据库文件（如果存在）
    db_path = os.path.join(instance_dir, 'university.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"删除旧数据库文件：{db_path}")
    
    print("正在配置数据库...")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    print(f"数据库URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"数据库追踪修改: {app.config['SQLALCHEMY_TRACK_MODIFICATIONS']}")
    
    # 创建所有表（如果不存在）
    with app.app_context():
        print("正在创建数据库表...")
        try:
            db.create_all()
            print("数据库表创建成功")
        except Exception as e:
            print(f"创建数据库表时出错：{str(e)}")
            return

        # 创建管理员账号
        try:
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                # 创建管理员用户
                admin = User(
                    username='admin',
                    role='admin',
                    name='管理员',
                    gender='男',
                    birth_date=datetime(1980, 1, 1),
                    email='admin@university.edu',
                    phone='13800000000',
                    department='管理部门',
                    hire_date=datetime(2010, 1, 1)
                )
                admin.set_password('admin123')
                db.session.add(admin)
                print('管理员账号创建成功！')
            else:
                print('管理员账号已存在')
        except Exception as e:
            print(f"创建管理员账号时出错：{str(e)}")
            return

        # 从Excel文件读取教师信息并创建账号
        try:
            excel_file = os.path.join(current_dir, '20241204教师名单(1).xls')
            print(f'正在读取Excel文件：{excel_file}')
            df = pd.read_excel(excel_file)
            print(f'成功读取到 {len(df)} 条教师记录')
            
            for _, row in df.iterrows():
                try:
                    username = str(row['姓名']).strip()  # 使用姓名作为登录名
                    if not username:  # 跳过空的姓名
                        continue
                        
                    # 检查用户是否已存在
                    existing_user = User.query.filter_by(username=username).first()
                    if not existing_user:
                        teacher = User(
                            username=username,
                            role='teacher',
                            name=username,
                            gender=str(row.get('性别', '')).strip(),
                            department=str(row.get('系部', '')).strip(),
                            email=str(row.get('邮箱', f'{username}@university.edu')).strip(),
                            phone=str(row.get('电话', '')).strip(),
                            education_level=str(row.get('学历', '')).strip(),
                            highest_title=str(row.get('职称', '')).strip(),
                            is_dual_teacher=bool(row.get('是否双师型', False)),
                            hire_date=row.get('入职日期', datetime.now()),
                            birth_date=row.get('出生日期', datetime(1980, 1, 1))
                        )
                        teacher.set_password('123456')  # 设置默认密码为123456
                        db.session.add(teacher)
                        print(f'教师账号 {username} 创建成功！')
                    else:
                        print(f'教师账号 {username} 已存在，跳过创建。')
                except Exception as e:
                    print(f'处理教师 {username} 的数据时出错：{str(e)}')
                    continue
                    
        except Exception as e:
            print(f'读取Excel文件或创建教师账号时出错：{str(e)}')
        
        # 更新指定用户的权限
        try:
            zhangyanpeng = User.query.filter_by(username='张艳鹏').first()
            if zhangyanpeng:
                zhangyanpeng.role = 'admin'
                print(f'已将用户 {zhangyanpeng.username} 的角色更新为 admin')
                
            wangpeng = User.query.filter_by(username='王鹏').first()
            if wangpeng:
                wangpeng.role = 'admin'
                print(f'已将用户 {wangpeng.username} 的角色更新为 admin')
        except Exception as e:
            print(f"更新用户权限时出错：{str(e)}")
        
        try:
            db.session.commit()
            print('数据库初始化完成！')
        except Exception as e:
            db.session.rollback()
            print(f'保存到数据库时出错：{str(e)}')

if __name__ == '__main__':
    init_db() 