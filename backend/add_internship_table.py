from app import db

def add_internship_table():
    """添加实习表"""
    # 创建实习表的 SQL 语句
    sql = """
    CREATE TABLE IF NOT EXISTS internship (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        college VARCHAR(100) NOT NULL,
        major_name VARCHAR(100) NOT NULL,
        major_type VARCHAR(20),
        class_name VARCHAR(50) NOT NULL,
        student_id VARCHAR(20) NOT NULL,
        student_name VARCHAR(50) NOT NULL,
        student_gender VARCHAR(10),
        student_phone VARCHAR(20),
        internship_type VARCHAR(20),
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        company_name VARCHAR(200) NOT NULL,
        province VARCHAR(50),
        city VARCHAR(50),
        detailed_address VARCHAR(200),
        base_type VARCHAR(20),
        internship_score VARCHAR(20),
        is_excellent_intern BOOLEAN DEFAULT 0,
        teacher_id INTEGER NOT NULL,
        external_teacher_name VARCHAR(50),
        external_teacher_position VARCHAR(50),
        external_teacher_phone VARCHAR(20),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES user(id)
    )
    """
    
    try:
        # 执行 SQL 语句
        db.session.execute(sql)
        db.session.commit()
        print("实习表创建成功！")
    except Exception as e:
        print(f"创建实习表时出错：{str(e)}")
        db.session.rollback()

if __name__ == '__main__':
    add_internship_table() 