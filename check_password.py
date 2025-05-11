from backend.app import db, User

# 查找卢长影的用户记录
teacher = User.query.filter_by(name='卢长影', role='teacher').first()

if teacher:
    print(f"用户名: {teacher.username}")
    # 打印所有属性
    for attr in dir(teacher):
        if not attr.startswith('_'):  # 跳过内部属性
            try:
                value = getattr(teacher, attr)
                if not callable(value):  # 跳过方法
                    print(f"{attr}: {value}")
            except:
                pass
else:
    print("未找到该教师记录") 