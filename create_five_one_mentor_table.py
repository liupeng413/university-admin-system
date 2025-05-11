import sqlite3
from datetime import datetime

def create_five_one_mentor_table():
    conn = sqlite3.connect('backend/university.db')
    cursor = conn.cursor()
    
    try:
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='five_one_mentor';")
        if cursor.fetchone() is None:
            # 创建表
            cursor.execute('''
                CREATE TABLE five_one_mentor (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id INTEGER NOT NULL,
                    student_name VARCHAR(50) NOT NULL,
                    student_id VARCHAR(20) NOT NULL,
                    class_name VARCHAR(50) NOT NULL,
                    photo_path VARCHAR(200),
                    status VARCHAR(20) DEFAULT 'pending',
                    review_comment TEXT,
                    reviewer_id INTEGER,
                    review_date DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (teacher_id) REFERENCES user(id),
                    FOREIGN KEY (reviewer_id) REFERENCES user(id)
                )
            ''')
            print("五业导师表创建成功！")
        else:
            print("五业导师表已存在。")
            
        conn.commit()
    except Exception as e:
        print(f"创建表时出错：{str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    create_five_one_mentor_table() 