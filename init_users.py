import pandas as pd
from werkzeug.security import generate_password_hash
import sqlite3
from datetime import datetime

def init_users():
    try:
        # 读取Excel文件
        df = pd.read_excel('20241204教师名单(1).xls')
        
        # 连接到数据库
        conn = sqlite3.connect('backend/university.db')
        cursor = conn.cursor()
        
        # 遍历Excel中的每一行
        for index, row in df.iterrows():
            teacher_name = str(row['姓名']).strip()  # 假设Excel中有"姓名"列
            if not teacher_name:
                continue
                
            # 生成密码哈希
            password_hash = generate_password_hash('123456')
            
            # 检查用户是否已存在
            cursor.execute('SELECT id FROM users WHERE username = ?', (teacher_name,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # 更新现有用户的密码
                cursor.execute('''
                    UPDATE users 
                    SET password_hash = ?
                    WHERE username = ?
                ''', (password_hash, teacher_name))
            else:
                # 插入新用户
                cursor.execute('''
                    INSERT INTO users (
                        username, 
                        password_hash,
                        role,
                        name,
                        gender,
                        ethnicity,
                        major,
                        department,
                        teaching_group,
                        highest_title,
                        education_level,
                        degree,
                        is_dual_teacher,
                        phone,
                        email,
                        employee_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    teacher_name,  # username
                    password_hash,  # password_hash
                    'teacher',  # role
                    teacher_name,  # name
                    row.get('性别', ''),  # gender
                    row.get('民族', ''),  # ethnicity
                    row.get('专业', ''),  # major
                    row.get('系部', ''),  # department
                    row.get('教研室', ''),  # teaching_group
                    row.get('职称', ''),  # highest_title
                    row.get('学历', ''),  # education_level
                    row.get('学位', ''),  # degree
                    row.get('双师型', ''),  # is_dual_teacher
                    str(row.get('联系电话', '')),  # phone
                    row.get('电子邮箱', ''),  # email
                    int(row['工号']) if pd.notna(row.get('工号')) else None  # employee_number
                ))
        
        # 提交事务
        conn.commit()
        print("用户初始化完成！")
        
    except Exception as e:
        print(f"初始化过程中出错：{str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    init_users() 