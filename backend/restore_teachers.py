from app import db, User
import pandas as pd

def restore_teachers():
    # 读取备份文件
    df = pd.read_excel('teacher_backup.xlsx')
    
    # 删除所有现有教师
    User.query.filter_by(role='teacher').delete()
    db.session.commit()
    
    # 重新添加教师
    for index, row in df.iterrows():
        teacher = User(
            username=f'teacher{index + 1}',
            name=row['name'],
            role='teacher',
            title=row['title'],
            subject_category=row['subject_category'],
            research_direction=row['research_direction'],
            address=row['address'],
            phone=row['phone']
        )
        db.session.add(teacher)
        print(f'添加教师 {row["name"]} (编号: teacher{index + 1})')
    
    db.session.commit()
    print(f'成功恢复 {len(df)} 名教师的信息')

if __name__ == '__main__':
    restore_teachers() 