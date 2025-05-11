import sqlite3
import os

def add_internship_tables():
    # 获取数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'university.db')
    
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 创建实习表
    try:
        c.execute('''
        CREATE TABLE IF NOT EXISTS teacher_internship (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            college VARCHAR(100) NOT NULL,
            major VARCHAR(100) NOT NULL,
            major_type VARCHAR(20) NOT NULL,
            class_name VARCHAR(50) NOT NULL,
            student_id VARCHAR(20) NOT NULL,
            student_name VARCHAR(50) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            student_phone VARCHAR(20) NOT NULL,
            internship_score VARCHAR(20) NOT NULL,
            is_excellent BOOLEAN DEFAULT 0,
            internship_type VARCHAR(20) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            internship_company VARCHAR(200) NOT NULL,
            province VARCHAR(50) NOT NULL,
            city VARCHAR(50) NOT NULL,
            address VARCHAR(200) NOT NULL,
            base_type VARCHAR(20) NOT NULL,
            teacher_id INTEGER NOT NULL,
            external_teacher_name VARCHAR(50) NOT NULL,
            external_teacher_title VARCHAR(50) NOT NULL,
            external_teacher_phone VARCHAR(20) NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES user (id)
        )
        ''')
        print("成功创建实习表")
        
        conn.commit()
    except Exception as e:
        print(f"创建表失败：{str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    add_internship_tables() 