import sqlite3
import os

def check_table_schema():
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'instance', 'university.db')
    print(f"检查数据库文件：{db_path}")
    
    if not os.path.exists(db_path):
        print(f"错误：数据库文件不存在！")
        return
        
    print(f"数据库文件大小：{os.path.getsize(db_path)} 字节")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("\n数据库中的所有表：")
        if tables:
            for table in tables:
                print(f"- {table[0]}")
                # 获取表的结构
                cursor.execute(f"PRAGMA table_info({table[0]});")
                columns = cursor.fetchall()
                print("  列信息：")
                for col in columns:
                    print(f"    - {col[1]} ({col[2]})")
        else:
            print("数据库中没有表！")
        
        # 检查graduation_projects表是否存在
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='graduation_projects';")
        schema = cursor.fetchone()
        
        if schema:
            print("\nGraduation Projects Table Schema:")
            print(schema[0])
        else:
            print("\ngraduation_projects表不存在！")
        
    except sqlite3.Error as e:
        print(f"数据库错误：{str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    check_table_schema() 