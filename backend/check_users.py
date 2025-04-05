from app import db, User

def list_users():
    """列出所有用户信息"""
    users = User.query.all()
    print("\n所有用户信息：")
    print("-" * 50)
    for user in users:
        print(f"用户名: {user.username}")
        print(f"姓名: {user.name}")
        print(f"角色: {user.role}")
        print("-" * 50)

if __name__ == '__main__':
    list_users() 