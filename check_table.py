import sqlite3

def check_table():
    conn = sqlite3.connect('backend/university.db')
    cursor = conn.cursor()
    
    # 检查表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='five_one_mentor';")
    if cursor.fetchone() is None:
        print("五业导师表不存在！")
        return
        
    # 获取表结构
    cursor.execute('PRAGMA table_info(five_one_mentor);')
    columns = cursor.fetchall()
    
    print("\n五业导师表结构:")
    print("=" * 80)
    print(f"{'序号':<5} {'字段名':<20} {'类型':<15} {'是否可空':<10} {'默认值':<20}")
    print("-" * 80)
    for col in columns:
        cid, name, type_, notnull, dflt_value, pk = col
        print(f"{cid:<5} {name:<20} {type_:<15} {'否' if notnull else '是':<10} {str(dflt_value):<20}")
    
    conn.close()

if __name__ == '__main__':
    check_table() 