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

def init_teachers():
    """初始化教师数据"""
    # 清除现有的教师数据
    User.query.filter_by(role='teacher').delete()
    db.session.commit()
    
    try:
        # 读取Excel文件
        df = pd.read_excel('../20241204教师名单(1).xls')
        
        # 遍历每一行数据
        for index, row in df.iterrows():
            try:
                # 处理日期格式
                birth_date = convert_date(row['出生年月'])
                work_start_date = convert_date(row['入校时间'])
                
                # 创建用户名（使用序号）
                username = f"teacher{index + 1}"
                
                # 创建新教师记录
                teacher = User(
                    username=username,
                    password_hash=generate_password_hash('123456'),  # 默认密码：123456
                    role='teacher',
                    name=row['姓名'],
                    gender=row['性别'],
                    ethnicity=process_ethnicity(row['民族']),
                    birth_date=birth_date,
                    major=row['专业'],
                    title=row['职称'],
                    bachelor_school=row['本科毕业院校'] if pd.notna(row['本科毕业院校']) else None,
                    master_school=row['硕士院校'] if pd.notna(row['硕士院校']) else None,
                    phd_school=row['博士院校'] if pd.notna(row['博士院校']) else None,
                    research_direction=row['研究方向'] if pd.notna(row['研究方向']) else None,
                    work_start_date=work_start_date
                )
                
                db.session.add(teacher)
                print(f'添加教师: {teacher.name} ({username})')
                
            except Exception as e:
                print(f'处理第 {index + 1} 行数据时出错: {str(e)}')
                continue
        
        # 提交所有更改
        db.session.commit()
        print('教师数据初始化完成！')
        
    except Exception as e:
        print(f'初始化过程出错: {str(e)}')
        db.session.rollback()

if __name__ == '__main__':
    init_teachers() 