import sqlite3
import random
from datetime import datetime, timedelta
import os

def add_test_records():
    try:
        # 连接到数据库
        conn = sqlite3.connect('backend/university.db')
        cursor = conn.cursor()
        
        # 获取一个教师ID
        cursor.execute("SELECT id, name FROM users WHERE role = 'teacher' LIMIT 1")
        teacher = cursor.fetchone()
        
        if not teacher:
            print("未找到教师记录")
            return
            
        teacher_id = teacher[0]
        teacher_name = teacher[1]
        
        # 生成测试数据
        for i in range(5):
            # 生成随机日期
            start_date = datetime.now() - timedelta(days=random.randint(1, 365))
            end_date = start_date + timedelta(days=random.randint(30, 90))
            
            # 插入实习记录
            cursor.execute('''
                INSERT INTO internships (
                    teacher_id,
                    student_name,
                    student_id,
                    class_name,
                    internship_type,
                    start_date,
                    end_date,
                    company_name,
                    province,
                    city,
                    detailed_address,
                    base_type,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                teacher_id,
                f'测试学生{i+1}',
                f'2024{str(i+1).zfill(4)}',
                '软件2301',
                '顶岗实习',
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'),
                f'测试公司{i+1}',
                '山东省',
                '济南市',
                f'测试地址{i+1}',
                '校外实习基地',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
        conn.commit()
        print(f"成功为教师 {teacher_name} 添加了5条测试记录")
        
    except Exception as e:
        print(f"添加记录失败：{str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    add_test_records() 