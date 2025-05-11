from app import app, db, User

def delete_user(username):
    """删除指定用户"""
    with app.app_context():
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                print(f"用户 {username} 已删除")
            else:
                print(f"用户 {username} 不存在")
        except Exception as e:
            print(f"删除用户时出错: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    delete_user('才  东')  # 删除包含空格的用户名 