from app import app, db
from models import User
import pandas as pd
from datetime import datetime
from werkzeug.security import generate_password_hash

def parse_date(date_str):
    if pd.isna(date_str):
        return None
    try:
        if isinstance(date_str, str) and '年' in date_str:
            return datetime.strptime(date_str, '%Y年').date()
        return pd.to_datetime(date_str).date()
    except:
        return None

def import_users():
    with app.app_context():
        try:
            # 读取Excel文件
            df = pd.read_excel('20241204教师名单(1).xls')
            
            # 遍历每一行数据
            for _, row in df.iterrows():
                # 检查用户是否已存在
                existing_user = User.query.filter_by(username=row['姓名']).first()
                
                if not existing_user:
                    # 创建新用户
                    user = User(
                        username=row['姓名'],
                        role='teacher',
                        name=row['姓名'],
                        gender=row['性别'],
                        ethnicity=row['民族'],
                        birth_date=parse_date(row['出生年月']),
                        political_status=row['政治面貌'],
                        hometown=row['籍贯'],
                        education_level=row['学历'],
                        degree=row['学位'],
                        position=row['职务'],
                        highest_title=row['职称'],
                        subject=row['学科类别'],
                        phone=str(int(row['联系电话'])) if pd.notna(row['联系电话']) else None,
                        address=row['家庭住址'],
                        work_start_date=parse_date(row['入校时间']),
                        id_number=str(int(row['身份证号'])) if pd.notna(row['身份证号']) else None
                    )
                    
                    # 设置默认密码为123456
                    user.set_password('123456')
                    
                    # 添加到数据库
                    db.session.add(user)
            
            # 提交所有更改
            db.session.commit()
            print("用户数据导入完成！")
            
        except Exception as e:
            print(f"导入过程中出错：{str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    import_users() 