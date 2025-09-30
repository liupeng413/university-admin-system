import sqlite3
import os

def check_tables():
    try:
        # 连接到数据库
        db_path = os.path.join('instance', 'university.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\n数据库中的所有表：")
        print("=" * 50)
        for table in tables:
            print(table[0])
            # 获取表的结构
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print("列：")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            print("-" * 50)
            
    except Exception as e:
        print(f"检查表时出错：{str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    check_tables() 