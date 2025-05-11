from app import app, db, User

def update_avatars():
    with app.app_context():
        try:
            # 获取所有用户
            users = User.query.all()
            
            for user in users:
                # 根据性别设置默认头像
                if user.gender == '男':
                    user.photo_path = 'img/boy.png'
                elif user.gender == '女':
                    user.photo_path = 'img/girl.png'
                else:
                    user.photo_path = 'img/boy.png'
            
            # 提交更改
            db.session.commit()
            print('头像更新完成！')
            
        except Exception as e:
            db.session.rollback()
            print(f'更新失败：{str(e)}')

if __name__ == '__main__':
    update_avatars() 