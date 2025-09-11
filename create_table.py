import sqlite3

# 连接到数据库
conn = sqlite3.connect('instance/university.db')
cursor = conn.cursor()

# 创建毕业设计表
cursor.execute('''
CREATE TABLE IF NOT EXISTS graduation_project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    graduation_year INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    major TEXT NOT NULL,
    class_name TEXT NOT NULL,
    project_title TEXT NOT NULL,
    project_type TEXT NOT NULL,
    score REAL NOT NULL,
    teacher_id INTEGER NOT NULL,
    grade TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
)
''')

# 提交更改并关闭连接
conn.commit()
conn.close() 