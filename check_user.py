import sqlite3

def check_user():
    conn = sqlite3.connect('backend/university.db')
    cursor = conn.cursor()
    
    # 查询所有用户信息
    print("\n所有用户信息:")
    print("=" * 80)
    cursor.execute("SELECT id, username, name, role FROM users")
    print(f"{'ID':<5} {'用户名':<15} {'姓名':<10} {'角色':<10}")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<10} {row[3]:<10}")
    
    conn.close()

if __name__ == '__main__':
    check_user() 