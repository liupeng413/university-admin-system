from app import app, db, User

def check_users():
    with app.app_context():
        users = User.query.all()
        if not users:
            print("用户表为空！")
        else:
            print("现有用户列表：")
            for user in users:
                print(f"用户名: {user.username}, 角色: {user.role}, 姓名: {user.name}")

if __name__ == '__main__':
    check_users() 