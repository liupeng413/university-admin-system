import sqlite3
import os

def add_missing_columns():
    """添加缺失的列到 teacher_internship 表"""
    try:
        # 获取数据库文件路径
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'university.db')
        
        # 连接到数据库
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # 获取现有的列
        c.execute("PRAGMA table_info(teacher_internship)")
        existing_columns = [column[1] for column in c.fetchall()]
        
        # 需要添加的列及其定义
        columns_to_add = {
            'college': 'VARCHAR(100)',
            'major': 'VARCHAR(100)',
            'major_type': 'VARCHAR(20)',
            'class_name': 'VARCHAR(50)',
            'student_id': 'VARCHAR(20)',
            'student_name': 'VARCHAR(50)',
            'gender': 'VARCHAR(10)',
            'student_phone': 'VARCHAR(20)',
            'internship_score': 'VARCHAR(20)',
            'is_excellent': 'BOOLEAN DEFAULT 0',
            'internship_type': 'VARCHAR(20)',
            'start_date': 'DATE',
            'end_date': 'DATE',
            'internship_company': 'VARCHAR(200)',
            'province': 'VARCHAR(50)',
            'city': 'VARCHAR(50)',
            'address': 'VARCHAR(200)',
            'base_type': 'VARCHAR(20)',
            'external_teacher_name': 'VARCHAR(50)',
            'external_teacher_title': 'VARCHAR(50)',
            'external_teacher_phone': 'VARCHAR(20)'
        }
        
        # 添加缺失的列
        for column_name, column_type in columns_to_add.items():
            if column_name not in existing_columns:
                try:
                    c.execute(f"ALTER TABLE teacher_internship ADD COLUMN {column_name} {column_type}")
                    print(f"成功添加列：{column_name}")
                except Exception as e:
                    print(f"添加列 {column_name} 时出错：{str(e)}")
        
        conn.commit()
        print("数据库更新完成")
        
    except Exception as e:
        print(f"更新数据库时出错：{str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    add_missing_columns() 