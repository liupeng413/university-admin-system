import sqlite3

def check_records():
    conn = sqlite3.connect('backend/university.db')
    cursor = conn.cursor()
    
    try:
        # 查询记录
        cursor.execute('''
            SELECT m.*, u.name as teacher_name 
            FROM five_one_mentor m 
            JOIN user u ON m.teacher_id = u.id
        ''')
        records = cursor.fetchall()
        
        if not records:
            print("五业导师表中没有记录")
            return
            
        print("\n五业导师记录:")
        print("=" * 100)
        print(f"{'ID':<5} {'学生姓名':<10} {'学号':<15} {'班级':<15} {'指导教师':<10} {'状态':<10} {'创建时间':<20}")
        print("-" * 100)
        
        for record in records:
            print(f"{record[0]:<5} {record[2]:<10} {record[3]:<15} {record[4]:<15} {record[-1]:<10} {record[6]:<10} {record[10]:<20}")
            
    except Exception as e:
        print(f"查询记录时出错：{str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    check_records() 