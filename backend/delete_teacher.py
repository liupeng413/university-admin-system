from app import db, User

def delete_teacher(name):
    """删除指定教师的信息"""
    try:
        # 查找教师
        teacher = User.query.filter_by(name=name, role='teacher').first()
        
        if teacher:
            # 删除教师
            db.session.delete(teacher)
            db.session.commit()
            print(f'成功删除教师 {name} 的信息')
        else:
            print(f'未找到名为 {name} 的教师')
            
    except Exception as e:
        db.session.rollback()
        print(f'删除失败：{str(e)}')

if __name__ == '__main__':
    delete_teacher('吴学农') 