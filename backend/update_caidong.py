from app import db, User
from sqlalchemy import or_

def update_caidong():
    try:
        # 使用模糊查询查找姓名包含"才"和"东"的教师
        teacher = User.query.filter(
            or_(
                User.name.like('%才%东%'),
                User.name.like('%才 东%')
            )
        ).first()
        
        if teacher:
            print(f'找到教师：{teacher.name}')
            # 更新姓名（去掉空格）
            teacher.name = '才东'
            # 设置用户名为 caidong
            teacher.username = 'caidong'
            
            # 提交更改
            db.session.commit()
            print(f'已更新教师信息：\n姓名: {teacher.name}\n用户名: {teacher.username}')
        else:
            print('未找到该教师')
        
    except Exception as e:
        db.session.rollback()
        print(f'更新失败：{str(e)}')

if __name__ == '__main__':
    update_caidong() 