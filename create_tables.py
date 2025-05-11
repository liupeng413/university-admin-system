import sqlite3
import os

def init_db():
    # 确保 instance 目录存在
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    # 连接到数据库
    conn = sqlite3.connect('instance/university.db')
    cursor = conn.cursor()
    
    # 读取 schema.sql 文件
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema = f.read()
    
    # 执行 SQL 语句
    cursor.executescript(schema)
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    
    print("数据库表创建成功！")

if __name__ == '__main__':
    init_db() 