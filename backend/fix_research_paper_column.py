import sqlite3

DB_PATH = 'backend/university.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE research_paper ADD COLUMN achievement_type VARCHAR(50);")
    print('字段 achievement_type 添加成功！')
except Exception as e:
    print('执行出错：', e)
finally:
    conn.commit()
    conn.close() 