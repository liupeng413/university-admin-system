from app import app, db, User
import sqlite3
import os

def reset_zhangyanpeng_password():
    try:
        # 连接到数据库
        db_path = os.path.join('instance', 'university.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 更新密码哈希
        new_password_hash = 'pbkdf2:sha256:260000$2NYvm5EUfaxoyFxW$9434194598c0a68bb7b51dca87e125b94948eea906995f3ebb09a33ba917a233'
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", 
                      (new_password_hash, '张艳鹏'))
        
        # 提交更改
        conn.commit()
        print("张艳鹏的密码已重置为：123456")
        
    except Exception as e:
        print(f"重置密码时出错：{str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    reset_zhangyanpeng_password() 