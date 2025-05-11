from app import app, db, User

def check_users():
    with app.app_context():
        users = User.query.all()
        print("\n所有用户信息:")
        print("=" * 100)
        print(f"{'ID':<5} {'用户名':<15} {'姓名':<10} {'角色':<10} {'性别':<6} {'职称':<10} {'学历':<10} {'部门':<15}")
        print("-" * 100)
        for user in users:
            print(f"{user.id:<5} {user.username:<15} {user.name:<10} {user.role:<10} "
                  f"{user.gender if user.gender else '':<6} "
                  f"{user.highest_title if user.highest_title else '':<10} "
                  f"{user.education_level if user.education_level else '':<10} "
                  f"{user.department if user.department else '':<15}")
        print("=" * 100)
        print(f"总计: {len(users)} 个用户")

if __name__ == '__main__':
    check_users() 