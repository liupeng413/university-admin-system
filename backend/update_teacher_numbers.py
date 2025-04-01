from app import db, User

def update_teacher_numbers():
    # 获取所有教师并按姓名排序
    teachers = User.query.filter_by(role='teacher').order_by(User.name).all()
    
    # 更新每个教师的编号
    for index, teacher in enumerate(teachers, 1):
        old_number = teacher.username
        new_number = f'teacher{index}'
        teacher.username = new_number
        print(f'更新教师 {teacher.name} 的编号: {old_number} -> {new_number}')
    
    try:
        db.session.commit()
        print(f'成功更新 {len(teachers)} 名教师的编号')
    except Exception as e:
        db.session.rollback()
        print(f'更新失败：{str(e)}')

if __name__ == '__main__':
    update_teacher_numbers() 