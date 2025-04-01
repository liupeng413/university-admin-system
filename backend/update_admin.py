from app import db, User

def update_user_role():
    user = User.query.filter_by(name='张艳鹏').first()
    if user:
        user.role = 'admin'
        db.session.commit()
        print(f'已将用户 {user.name} (用户名: {user.username}) 的角色更新为管理员')
    else:
        print('未找到用户：张艳鹏')

if __name__ == '__main__':
    update_user_role() 