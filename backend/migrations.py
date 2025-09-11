from app import db
import sqlite3
from datetime import datetime
import os

def add_id_number_column():
    """添加身份证号字段"""
    try:
        db.engine.execute('ALTER TABLE user ADD COLUMN id_number VARCHAR(18)')
        print("成功添加身份证号字段")
    except Exception as e:
        print(f"添加字段失败：{str(e)}")

def add_department_column():
    """添加部门字段"""
    try:
        db.engine.execute('ALTER TABLE user ADD COLUMN department VARCHAR(100)')
        print("成功添加部门字段")
    except Exception as e:
        print(f"添加字段失败：{str(e)}")

def add_email_column():
    """添加电子邮件字段"""
    try:
        db.engine.execute('ALTER TABLE user ADD COLUMN email VARCHAR(100)')
        print("成功添加电子邮件字段")
    except Exception as e:
        print(f"添加字段失败：{str(e)}")

def add_political_status_column():
    """添加政治面貌字段"""
    try:
        db.engine.execute('ALTER TABLE user ADD COLUMN political_status VARCHAR(20)')
        print("成功添加政治面貌字段")
    except Exception as e:
        print(f"添加字段失败：{str(e)}")

def add_party_join_date_column():
    """添加入党时间字段"""
    try:
        db.engine.execute('ALTER TABLE user ADD COLUMN party_join_date DATE')
        print("成功添加入党时间字段")
    except Exception as e:
        print(f"添加字段失败：{str(e)}")

def add_photo_path_column():
    """添加照片路径字段"""
    try:
        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()
        cursor.execute('ALTER TABLE user ADD COLUMN photo_path TEXT')
        conn.commit()
        print("成功添加照片路径字段")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("照片路径字段已存在")
        else:
            print(f"添加照片路径字段失败: {e}")
    finally:
        conn.close()

def add_education_columns():
    """添加学历学位相关字段"""
    try:
        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()
        
        # 添加学历字段
        cursor.execute('ALTER TABLE user ADD COLUMN education_level VARCHAR(20)')
        # 添加学位字段
        cursor.execute('ALTER TABLE user ADD COLUMN degree VARCHAR(20)')
        # 添加获得学历时间字段
        cursor.execute('ALTER TABLE user ADD COLUMN education_date DATE')
        # 添加获得学位时间字段
        cursor.execute('ALTER TABLE user ADD COLUMN degree_date DATE')
        
        conn.commit()
        print("成功添加学历学位相关字段")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("学历学位相关字段已存在")
        else:
            print(f"添加学历学位相关字段失败: {e}")
    finally:
        conn.close()

def add_career_start_date():
    """添加参加工作时间字段"""
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    
    try:
        # 检查字段是否已存在
        c.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in c.fetchall()]
        
        if 'career_start_date' not in columns:
            # 添加新字段
            c.execute('ALTER TABLE user ADD COLUMN career_start_date DATE')
            print("成功添加参加工作时间字段")
        else:
            print("参加工作时间字段已存在")
            
        conn.commit()
    except Exception as e:
        print(f"添加字段失败：{str(e)}")
        conn.rollback()
    finally:
        conn.close()

def add_highest_title_columns():
    """添加最高级职称相关字段"""
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    
    try:
        # 检查字段是否已存在
        c.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in c.fetchall()]
        
        if 'highest_title' not in columns:
            c.execute('ALTER TABLE user ADD COLUMN highest_title VARCHAR(50)')
            print("成功添加最高级职称字段")
        else:
            print("最高级职称字段已存在")
            
        if 'highest_title_date' not in columns:
            c.execute('ALTER TABLE user ADD COLUMN highest_title_date DATE')
            print("成功添加最高级职称获得时间字段")
        else:
            print("最高级职称获得时间字段已存在")
            
        conn.commit()
    except Exception as e:
        print(f"添加字段失败：{str(e)}")
        conn.rollback()
    finally:
        conn.close()

def migrate():
    # 获取数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'university.db')
    
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 添加新字段
    try:
        c.execute('ALTER TABLE user ADD COLUMN teaching_team VARCHAR(100);')
        print("成功添加 teaching_team 字段")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e):
            print("teaching_team 字段已存在")
        else:
            print(f"添加 teaching_team 字段时出错: {e}")

    try:
        c.execute('ALTER TABLE user ADD COLUMN research_team VARCHAR(100);')
        print("成功添加 research_team 字段")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e):
            print("research_team 字段已存在")
        else:
            print(f"添加 research_team 字段时出错: {e}")

    try:
        c.execute('ALTER TABLE user ADD COLUMN project_group VARCHAR(100);')
        print("成功添加 project_group 字段")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e):
            print("project_group 字段已存在")
        else:
            print(f"添加 project_group 字段时出错: {e}")

    try:
        c.execute('ALTER TABLE user ADD COLUMN party_branch VARCHAR(100);')
        print("成功添加 party_branch 字段")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e):
            print("party_branch 字段已存在")
        else:
            print(f"添加 party_branch 字段时出错: {e}")
    
    # 提交更改
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_id_number_column()
    add_department_column()
    add_email_column()
    add_political_status_column()
    add_party_join_date_column()
    add_photo_path_column()
    add_education_columns()
    add_career_start_date()
    add_highest_title_columns()
    migrate() 