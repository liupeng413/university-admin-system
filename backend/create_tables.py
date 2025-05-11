from app import db

def create_tables():
    # 创建所有表
    db.create_all()
    print("数据库表创建成功！")

if __name__ == '__main__':
    create_tables() 