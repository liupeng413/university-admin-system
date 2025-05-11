from backend.app import db, User

# 查找卢长影的用户记录
teacher = User.query.filter_by(name='卢长影', role='teacher').first()

if teacher:
    # 更新用户名
    teacher.username = 'luchangying'
    
    try:
        db.session.commit()
        print("用户名更新成功！")
        print(f"新用户名: {teacher.username}")
    except Exception as e:
        db.session.rollback()
        print(f"更新失败：{str(e)}")
else:
    print("未找到该教师记录") 