from app import db, User
import pandas as pd

def update_contact_info():
    """从Excel文件更新教师的联系信息、研究方向和学科类别"""
    try:
        # 读取Excel文件
        df = pd.read_excel('../20241204教师名单(1).xls')
        
        # 获取所有教师
        teachers = User.query.filter_by(role='teacher').all()
        
        # 创建姓名到信息的映射
        address_dict = dict(zip(df['姓名'], df['家庭住址']))
        phone_dict = dict(zip(df['姓名'], df['联系电话']))
        research_dict = dict(zip(df['姓名'], df['研究方向']))
        major_dict = dict(zip(df['姓名'], df['学科类别']))
        title_dict = dict(zip(df['姓名'], df['职称']))
        hometown_dict = dict(zip(df['姓名'], df['籍贯']))
        
        # 更新每个教师的信息
        for teacher in teachers:
            if teacher.name in address_dict:
                # 更新家庭住址
                address = address_dict[teacher.name]
                if pd.notna(address):
                    teacher.address = str(address).strip()
                    print(f'更新教师 {teacher.name} 的家庭住址为: {teacher.address}')
                else:
                    teacher.address = None
                    print(f'教师 {teacher.name} 的家庭住址为空')
                
                # 更新联系电话
                phone = phone_dict[teacher.name]
                if pd.notna(phone):
                    # 处理电话号码可能是数字格式的情况
                    if isinstance(phone, (int, float)):
                        phone = str(int(phone))
                    teacher.phone = str(phone).strip()
                    print(f'更新教师 {teacher.name} 的联系电话为: {teacher.phone}')
                else:
                    teacher.phone = None
                    print(f'教师 {teacher.name} 的联系电话为空')
                
                # 更新研究方向
                research = research_dict[teacher.name]
                if pd.notna(research):
                    teacher.research_direction = str(research).strip()
                    print(f'更新教师 {teacher.name} 的研究方向为: {teacher.research_direction}')
                else:
                    teacher.research_direction = None
                    print(f'教师 {teacher.name} 的研究方向为空')
                
                # 更新学科类别
                major = major_dict[teacher.name]
                if pd.notna(major):
                    teacher.major = str(major).strip()
                    print(f'更新教师 {teacher.name} 的学科类别为: {teacher.major}')
                else:
                    teacher.major = None
                    print(f'教师 {teacher.name} 的学科类别为空')
                
                # 更新籍贯
                hometown = hometown_dict[teacher.name]
                if pd.notna(hometown):
                    teacher.hometown = str(hometown).strip()
                    print(f'更新教师 {teacher.name} 的籍贯为: {teacher.hometown}')
                else:
                    teacher.hometown = None
                    print(f'教师 {teacher.name} 的籍贯为空')
                
                # 更新职称
                title = title_dict[teacher.name]
                if pd.notna(title):
                    title_str = str(title).strip()
                    # 如果职称为空、未定职或未定级，设置为助教
                    if not title_str or title_str in ['未定职', '未定级']:
                        teacher.title = "助教"
                        print(f'教师 {teacher.name} 的职称设置为: 助教')
                    else:
                        teacher.title = title_str
                        print(f'更新教师 {teacher.name} 的职称为: {teacher.title}')
                else:
                    teacher.title = "助教"
                    print(f'教师 {teacher.name} 的职称设置为: 助教')
        
        # 提交更改
        db.session.commit()
        print('教师信息更新完成！')
        
    except Exception as e:
        db.session.rollback()
        print(f'更新失败：{str(e)}')

if __name__ == '__main__':
    update_contact_info() 