import pandas as pd
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def import_teachers():
    # 读取Excel文件
    df = pd.read_excel('20241204教师名单(1).xls')
    
    # 遍历每一行数据
    for index, row in df.iterrows():
        # 检查用户是否已存在
        existing_user = User.query.filter_by(username=row['姓名']).first()
        if existing_user:
            print(f"用户 {row['姓名']} 已存在，跳过")
            continue
            
        # 创建新用户
        user = User(
            username=row['姓名'],
            real_name=row['姓名'],
            gender=row['性别'],
            ethnicity=row['民族'],
            birth_date=row['出生年月'],
            entry_date=row['入校时间'],
            political_status=row['政治面貌'],
            hometown=row['籍贯'],
            subject=row['学科类别'],
            education=row['学历'],
            title=row['职称'],
            id_number=str(int(row['身份证号'])) if not pd.isna(row['身份证号']) else None,
            address=row['家庭住址'],
            phone=str(int(row['联系电话'])) if not pd.isna(row['联系电话']) else None,
            role='teacher'  # 设置角色为教师
        )
        
        # 设置默认密码为身份证号后6位
        if not pd.isna(row['身份证号']):
            default_password = str(int(row['身份证号']))[-6:]
            user.set_password(default_password)
        else:
            # 如果没有身份证号，使用默认密码123456
            user.set_password('123456')
            
        # 添加到数据库
        db.session.add(user)
        print(f"添加用户: {row['姓名']}")
    
    # 提交所有更改
    try:
        db.session.commit()
        print("所有教师数据导入成功！")
    except Exception as e:
        db.session.rollback()
        print(f"导入过程中发生错误: {str(e)}")

if __name__ == '__main__':
    with app.app_context():
        import_teachers() 