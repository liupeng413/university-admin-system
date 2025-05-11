import pandas as pd
from app import app, db, User
from datetime import datetime

def parse_date(date_str):
    if pd.isna(date_str):
        return None
    try:
        if isinstance(date_str, str) and ('年' in date_str or '-' in date_str or '/' in date_str):
            # 支持多种日期格式
            for fmt in ('%Y年', '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%Y-%m', '%Y/%m'):
                try:
                    return datetime.strptime(date_str, fmt).date()
                except:
                    continue
        return pd.to_datetime(date_str).date()
    except:
        return None

def update_teachers_from_xls(xls_path):
    df = pd.read_excel(xls_path)
    updated_count = 0
    with app.app_context():
        for _, row in df.iterrows():
            excel_name = str(row.get('姓名')).strip()
            if not excel_name:
                continue
            # 用username字段匹配
            user = User.query.filter_by(username=excel_name, role='teacher').first()
            if not user:
                continue  # 只更新已存在的教师
            # 同步name字段
            user.name = excel_name
            # 更新基本信息字段
            user.gender = row.get('性别') or user.gender
            user.ethnicity = row.get('民族') or user.ethnicity
            user.birth_date = parse_date(row.get('出生年月')) or user.birth_date
            user.political_status = row.get('政治面貌') or user.political_status
            user.hometown = row.get('籍贯') or user.hometown
            user.education_level = row.get('学历') or user.education_level
            user.degree = row.get('学位') or user.degree
            user.position = row.get('职务') or user.position
            user.highest_title = row.get('职称') or user.highest_title
            user.subject = row.get('学科类别') or user.subject
            user.phone = str(row.get('联系电话')) if pd.notna(row.get('联系电话')) else user.phone
            user.address = row.get('家庭住址') or user.address
            user.work_start_date = parse_date(row.get('入校时间')) or user.work_start_date
            user.id_number = str(row.get('身份证号')) if pd.notna(row.get('身份证号')) else user.id_number
            updated_count += 1
        db.session.commit()
    print(f"已更新 {updated_count} 位教师的基本信息。");

if __name__ == '__main__':
    update_teachers_from_xls('20241204教师名单(1).xls') 