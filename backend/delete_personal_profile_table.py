import sqlite3

DB_PATH = 'backend/university.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("DROP TABLE IF EXISTS personal_profile;")
    print('personal_profile 表已删除！')
except Exception as e:
    print('执行出错：', e)
finally:
    conn.commit()
    conn.close() 