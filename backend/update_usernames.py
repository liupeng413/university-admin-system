from app import db, User
from pypinyin import pinyin, Style

def update_usernames():
    try:
        # 获取所有教师
        teachers = User.query.filter_by(role='teacher').all()
        
        for teacher in teachers:
            if teacher.name:
                # 获取姓名的拼音，并转换为小写
                pinyin_list = pinyin(teacher.name, style=Style.NORMAL)
                # 将拼音列表展平为一个字符串
                username = ''.join([''.join(p) for p in pinyin_list])
                # 更新用户名
                teacher.username = username
                print(f'更新教师 {teacher.name} 的用户名为: {username}')
        
        # 提交更改
        db.session.commit()
        print('教师用户名更新完成！')
        
    except Exception as e:
        db.session.rollback()
        print(f'更新失败：{str(e)}')

if __name__ == '__main__':
    update_usernames() 