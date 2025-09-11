from backend.app import db, User

# 查找吴学农的用户记录
teacher = User.query.filter_by(name='吴学农', role='teacher').first()

if teacher:
    # 保留用户名、密码和角色，清空其他信息
    teacher.name = '卢长影'
    teacher.gender = None
    teacher.ethnicity = None
    teacher.birth_date = None
    teacher.id_number = None
    teacher.political_status = None
    teacher.party_join_date = None
    teacher.party_branch = None
    teacher.hometown = None
    teacher.position = None
    teacher.address = None
    teacher.phone = None
    teacher.email = None
    teacher.education_level = None
    teacher.degree = None
    teacher.education_date = None
    teacher.degree_date = None
    teacher.bachelor_school = None
    teacher.master_school = None
    teacher.phd_school = None
    teacher.research_direction = None
    teacher.work_start_date = None
    teacher.career_start_date = None
    teacher.highest_title = None
    teacher.highest_title_date = None
    teacher.employee_number = None
    teacher.department = None
    teacher.photo_path = None
    teacher.subject = None
    teacher.teaching_team = None
    teacher.research_team = None
    teacher.project_group = None
    teacher.major = None
    teacher.teaching_group = None
    teacher.is_dual_teacher = None
    teacher.award_title = None
    teacher.talent_title = None
    
    try:
        db.session.commit()
        print("教师信息更新成功！")
    except Exception as e:
        db.session.rollback()
        print(f"更新失败：{str(e)}")
else:
    print("未找到该教师记录") 