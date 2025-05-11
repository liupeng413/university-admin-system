import pandas as pd
from app import app, db, User
from werkzeug.security import generate_password_hash
import os

def reimport_all_teachers():
    """重新导入所有教师信息"""
    with app.app_context():
        try:
            # 清空用户表中的教师记录（保留管理员）
            User.query.filter_by(role='teacher').delete()
            db.session.commit()
            print("已清空教师记录")
            
            # 读取Excel文件
            excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '20241204教师名单(1).xls')
            df = pd.read_excel(excel_path)
            
            # 定义管理员列表
            admin_list = ['张艳鹏', '王鹏']
            
            # 遍历每一行数据
            for index, row in df.iterrows():
                # 去掉姓名中的空格作为用户名
                username = row['姓名'].replace(" ", "")
                
                # 判断是否为管理员
                role = 'admin' if username in admin_list else 'teacher'
                
                # 创建新用户
                user = User(
                    username=username,
                    password_hash=generate_password_hash('123456'),  # 设置初始密码为123456
                    role=role,  # 根据是否在管理员列表中设置角色
                    name=row['姓名'].strip(),  # 保留原始姓名，但去掉首尾空格
                    gender=row.get('性别', ''),
                    ethnicity=row.get('民族', ''),
                    major=row.get('专业', ''),
                    department=row.get('系部', ''),
                    teaching_group=row.get('教研室', ''),
                    highest_title=row.get('职称', ''),
                    education_level=row.get('学历', ''),
                    degree=row.get('学位', ''),
                    is_dual_teacher=row.get('双师型', ''),
                    phone=str(row.get('联系电话', '')),
                    email=row.get('电子邮箱', ''),
                    employee_number=int(row['工号']) if pd.notna(row.get('工号')) else None
                )
                db.session.add(user)
                print(f"添加{'管理员' if role == 'admin' else '教师'}: {username}")
            
            db.session.commit()
            print("所有教师信息导入完成！")
            
        except Exception as e:
            print(f"导入出错: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    reimport_all_teachers() 