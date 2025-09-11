import pandas as pd
from backend.models import db, User
from backend.app import app

def safe_str(val):
    if pd.isna(val):
        return ""
    try:
        return str(int(float(val)))
    except Exception:
        return str(val).strip()

def import_id_phone_from_excel(excel_path):
    df = pd.read_excel(excel_path)
    with app.app_context():
        for _, row in df.iterrows():
            name = str(row.get('姓名', '')).strip()
            id_number = safe_str(row.get('身份证号', ''))
            phone = safe_str(row.get('联系电话', ''))
            if not name:
                continue  # 跳过无效数据
            user = User.query.filter_by(name=name).first()
            if user:
                user.id_number = id_number
                user.phone = phone
        db.session.commit()
    print("根据姓名，身份证号和联系电话已更新（字符串格式）！")

if __name__ == '__main__':
    import_id_phone_from_excel('backend/20241204教师名单(1).xls') 