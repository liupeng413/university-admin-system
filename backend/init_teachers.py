import pandas as pd
from app import db, User
from werkzeug.security import generate_password_hash
from datetime import datetime

def convert_date(date_str):
    if pd.isna(date_str):
        return None
    try:
        # 尝试直接转换日期
        return pd.to_datetime(date_str).date()
    except:
        try:
            # 尝试处理特殊格式
            if isinstance(date_str, str):
                # 移除可能的空格
                date_str = date_str.strip()
                # 处理 "yyyy.mm" 格式
                if '.' in date_str:
                    year, month = date_str.split('.')
                    return datetime(int(year), int(month), 1).date()
                # 处理 "yyyy年mm月" 格式
                elif '年' in date_str:
                    date_str = date_str.replace('年', '.').replace('月', '')
                    year, month = date_str.split('.')
                    return datetime(int(year), int(month), 1).date()
        except:
            pass
    return None

def process_ethnicity(ethnicity):
    """处理民族字段，确保格式统一"""
    if not ethnicity or pd.isna(ethnicity):
        return '汉族'  # 默认值
    # 如果已经是"族"结尾，就直接返回
    if str(ethnicity).endswith('族'):
        return ethnicity
    # 否则添加"族"后缀
    return str(ethnicity) + '族'

def update_admin_teacher_list():
    """为管理员更新教师列表"""
    try:
        # 获取所有教师ID
        teacher_ids = [str(teacher.id) for teacher in User.query.filter_by(role='teacher').all()]
        teacher_list = ','.join(teacher_ids)
        
        # 为管理员添加所有教师列表
        admin_users = User.query.filter(User.username.in_(['zhangyanpeng', 'wangpeng'])).all()
        for admin in admin_users:
            if admin:
                admin.teacher_list = teacher_list
                print(f'为管理员 {admin.username} 添加了所有教师列表')
        
        db.session.commit()
        print('管理员教师列表更新完成！')
        
    except Exception as e:
        print(f'更新管理员教师列表时出错: {str(e)}')
        db.session.rollback()

if __name__ == '__main__':
    update_admin_teacher_list() 