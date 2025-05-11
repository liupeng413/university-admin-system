import pandas as pd
from app import app, db, User
from werkzeug.security import generate_password_hash
import os

def import_single_teacher(target_name):
    """导入单个教师信息"""
    with app.app_context():
        try:
            # 读取Excel文件
            excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '20241204教师名单(1).xls')
            df = pd.read_excel(excel_path)
            
            # 查找目标教师
            teacher_data = df[df['姓名'].str.strip() == target_name.strip()]
            
            if teacher_data.empty:
                print(f"未找到教师: {target_name}")
                return
                
            row = teacher_data.iloc[0]
            username = row['姓名'].replace(" ", "")  # 去掉空格
            existing_user = User.query.filter_by(username=username).first()
            
            if not existing_user:
                # 创建新用户
                user = User(
                    username=username,
                    password_hash=generate_password_hash('123456'),  # 设置初始密码为123456
                    role='teacher',
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
                db.session.commit()
                print(f"成功添加教师: {username}")
            else:
                print(f"教师已存在: {username}")
            
        except Exception as e:
            print(f"导入出错: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    import_single_teacher('才  东') 