from app import db, Internship

def check_internships():
    print("实习表的所有字段：", [column.name for column in Internship.__table__.columns])
    print("\n是否存在 start_date 字段：", 'start_date' in [column.name for column in Internship.__table__.columns])
    print("是否存在 end_date 字段：", 'end_date' in [column.name for column in Internship.__table__.columns])
    
    print("\n实习数据示例：")
    internships = Internship.query.limit(5).all()
    for internship in internships:
        print(f"ID: {internship.id}")
        print(f"学生姓名: {internship.student_name}")
        print(f"开始日期: {internship.start_date}")
        print(f"结束日期: {internship.end_date}")
        print("---")

if __name__ == '__main__':
    check_internships() 