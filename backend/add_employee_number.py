import sqlite3

def add_employee_number():
    # 连接到数据库
    conn = sqlite3.connect('backend/university.db')
    cursor = conn.cursor()
    
    try:
        # 添加工号列
        cursor.execute('ALTER TABLE user ADD COLUMN employee_number INTEGER DEFAULT 0')
        conn.commit()
        print("成功添加工号字段！")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("工号字段已存在")
        else:
            print(f"发生错误：{str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_employee_number() 