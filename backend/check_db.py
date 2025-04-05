from app import db, User

def check_database():
    """检查数据库结构和数据"""
    # 获取表的所有列
    columns = [column.name for column in User.__table__.columns]
    print("用户表的所有字段：", columns)
    
    # 检查是否有 id_number 字段
    print("\n是否存在 id_number 字段：", 'id_number' in columns)
    
    # 查看一个用户的数据示例
    user = User.query.first()
    if user:
        print("\n用户数据示例：")
        print(f"ID: {user.id}")
        print(f"姓名: {user.name}")
        print(f"身份证号: {user.id_number}")
    else:
        print("\n数据库中没有用户数据")

if __name__ == '__main__':
    check_database() 