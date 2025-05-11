from app import db, User
import os
import sqlite3

def check_database():
    db_path = os.path.join('instance', 'university.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取用户表的所有字段
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    print("用户表的所有字段：", [col[1] for col in columns])
    
    # 查询所有用户
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    if users:
        print(f"\n找到 {len(users)} 个用户：")
        for user in users:
            print(f"ID: {user[0]}")
            print(f"用户名: {user[1]}")
            print(f"姓名: {user[2]}")
            print(f"角色: {user[4]}")
            print("-" * 30)
    else:
        print("\n数据库中没有用户数据")
    
    conn.close()

def check_teachers():
    db_path = os.path.join('instance', 'university.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询所有教师
    cursor.execute("SELECT id, name, role, gender, birth_date, education_level, highest_title FROM users WHERE role='teacher'")
    teachers = cursor.fetchall()
    
    if teachers:
        print(f"\n找到 {len(teachers)} 名教师：")
        for teacher in teachers:
            print(f"ID: {teacher[0]}")
            print(f"姓名: {teacher[1]}")
            print(f"性别: {teacher[3]}")
            print(f"学历: {teacher[5]}")
            print(f"职称: {teacher[6]}")
            print("-" * 30)
    else:
        print("\n未找到任何教师记录")
    
    conn.close()

def check_table_schema():
    db_path = os.path.join('instance', 'university.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取所有表的名称
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n数据库中的所有表：")
    for table in tables:
        print(f"\n表名: {table[0]}")
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        print("列信息:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    conn.close()

def check_tables():
    db_path = os.path.join('instance', 'university.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取所有表的名称
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if tables:
        print("\n数据库中存在的表：")
        for table in tables:
            print(f"- {table[0]}")
            # 获取表的结构
            cursor.execute(f"PRAGMA table_info({table[0]});")
            columns = cursor.fetchall()
            print("  列信息:")
            for col in columns:
                print(f"    {col[1]} ({col[2]})")
            print()
    else:
        print("\n数据库中没有任何表！")
    
    conn.close()

def check_zhangyanpeng():
    db_path = os.path.join('instance', 'university.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查用户表
    cursor.execute("SELECT * FROM users WHERE username='张艳鹏'")
    user = cursor.fetchone()
    
    if user:
        print("\n找到张艳鹏的用户信息：")
        print(f"ID: {user[0]}")
        print(f"用户名: {user[1]}")
        print(f"密码哈希: {user[2]}")
        print(f"角色: {user[3]}")
        print(f"姓名: {user[4]}")
        print(f"性别: {user[5]}")
        print(f"部门: {user[11]}")
    else:
        print("\n未找到张艳鹏的用户信息！")
    
    conn.close()

if __name__ == '__main__':
    check_zhangyanpeng() 