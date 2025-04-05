import sqlite3

def update_photo_paths():
    try:
        # 连接到数据库
        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()

        # 清空所有用户的照片路径
        cursor.execute("""
            UPDATE user 
            SET photo_path = NULL
        """)

        # 提交更改
        conn.commit()
        print("成功重置照片路径")

    except Exception as e:
        print(f"更新失败：{str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    update_photo_paths() 