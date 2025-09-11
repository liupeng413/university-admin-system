from app import db, User
import pandas as pd

def backup_teachers():
    # 获取所有教师
    teachers = User.query.filter_by(role='teacher').order_by(User.name).all()
    
    # 创建数据列表
    data = []
    for teacher in teachers:
        data.append({
            'name': teacher.name,
            'title': teacher.title,
            'subject_category': teacher.subject_category,
            'research_direction': teacher.research_direction,
            'address': teacher.address,
            'phone': teacher.phone
        })
    
    # 创建DataFrame并保存到Excel
    df = pd.DataFrame(data)
    df.to_excel('teacher_backup.xlsx', index=False)
    print(f'成功备份 {len(teachers)} 名教师的信息到 teacher_backup.xlsx')

if __name__ == '__main__':
    backup_teachers() 