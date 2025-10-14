from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student
    name = db.Column(db.String(80))
    gender = db.Column(db.String(10))
    birth_date = db.Column(db.Date)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    
    # 基本信息
    employee_number = db.Column(db.String(20))
    ethnicity = db.Column(db.String(50))  # 民族
    id_number = db.Column(db.String(18))  # 身份证号
    political_status = db.Column(db.String(50))  # 政治面貌
    party_join_date = db.Column(db.Date)  # 入党时间
    party_branch = db.Column(db.String(100))  # 所属党支部
    hometown = db.Column(db.String(100))  # 籍贯
    address = db.Column(db.String(200))  # 家庭住址
    
    # 教育背景
    education_level = db.Column(db.String(50))  # 学历
    education_date = db.Column(db.Date)  # 获得学历时间
    degree = db.Column(db.String(50))  # 学位
    degree_date = db.Column(db.Date)  # 获得学位时间
    bachelor_school = db.Column(db.String(100))  # 本科毕业学校
    master_school = db.Column(db.String(100))  # 硕士毕业学校
    phd_school = db.Column(db.String(100))  # 博士毕业学校
    
    # 工作信息
    major = db.Column(db.String(100))  # 专业
    teaching_group = db.Column(db.String(100))  # 教研室
    is_dual_teacher = db.Column(db.String(10))  # 是否双师
    award_title = db.Column(db.String(100))  # 获得奖励称号
    talent_title = db.Column(db.String(100))  # 人才称号
    research_direction = db.Column(db.String(200))  # 研究方向
    work_start_date = db.Column(db.Date)  # 入校时间
    career_start_date = db.Column(db.Date)  # 参加工作时间
    highest_title = db.Column(db.String(50))  # 最高级职称
    highest_title_date = db.Column(db.Date)  # 获得最高级职称时间
    position = db.Column(db.String(50))  # 职务
    subject = db.Column(db.String(50))  # 学科
    department = db.Column(db.String(100))  # 所属院系
    photo_path = db.Column(db.String(200))  # 照片路径
    
    # 教师特有字段
    hire_date = db.Column(db.Date)             # 入职日期
    
    def __init__(self, username, password=None, role='student', **kwargs):
        self.username = username
        if password:
            self.set_password(password)
        self.role = role
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        def safe_str(val):
            if val is None:
                return ""
            try:
                return str(int(float(val)))
            except Exception:
                return str(val)
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date.strftime('%Y-%m-%d') if self.birth_date else None,
            'email': self.email,
            'phone': safe_str(self.phone),
            'education_level': self.education_level,
            'highest_title': self.highest_title,
            'is_dual_teacher': self.is_dual_teacher,
            'department': self.department,
            'hire_date': self.hire_date.strftime('%Y-%m-%d') if self.hire_date else None,
            'photo_path': self.photo_path,
            'employee_number': self.employee_number,
            'ethnicity': self.ethnicity,
            'id_number': safe_str(self.id_number),
            'political_status': self.political_status,
            'party_join_date': self.party_join_date.strftime('%Y-%m-%d') if self.party_join_date else None,
            'party_branch': self.party_branch,
            'hometown': self.hometown,
            'address': self.address,
            'education_date': self.education_date.strftime('%Y-%m-%d') if self.education_date else None,
            'degree': self.degree,
            'degree_date': self.degree_date.strftime('%Y-%m-%d') if self.degree_date else None,
            'bachelor_school': self.bachelor_school,
            'master_school': self.master_school,
            'phd_school': self.phd_school,
            'major': self.major,
            'teaching_group': self.teaching_group,
            'award_title': self.award_title,
            'talent_title': self.talent_title,
            'research_direction': self.research_direction,
            'work_start_date': self.work_start_date.strftime('%Y-%m-%d') if self.work_start_date else None,
            'career_start_date': self.career_start_date.strftime('%Y-%m-%d') if self.career_start_date else None,
            'highest_title_date': self.highest_title_date.strftime('%Y-%m-%d') if self.highest_title_date else None,
            'position': self.position,
            'subject': self.subject
        }

    @property
    def age(self):
        if self.birth_date:
            today = datetime.now()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

class GraduationProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)  # 学生姓名
    student_id = db.Column(db.String(20), nullable=False)  # 学号
    major = db.Column(db.String(100), nullable=False)  # 专业
    class_name = db.Column(db.String(50), nullable=False)  # 班级
    graduation_year = db.Column(db.Integer, nullable=False)  # 毕业年份
    project_title = db.Column(db.String(200), nullable=False)  # 论文题目
    project_type = db.Column(db.String(20), nullable=False)  # 形式（毕业设计/毕业论文）
    score = db.Column(db.Float, nullable=False)  # 论文成绩
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 指导教师ID
    grade = db.Column(db.String(10), nullable=False)  # 论文等级
    created_at = db.Column(db.DateTime, nullable=True, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    teacher = db.relationship('User', backref=db.backref('graduation_projects', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'student_name': self.student_name,
            'student_id': self.student_id,
            'major': self.major,
            'class_name': self.class_name,
            'graduation_year': self.graduation_year,
            'project_title': self.project_title,
            'project_type': self.project_type,
            'score': self.score,
            'teacher_id': self.teacher_id,
            'grade': self.grade,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class TeacherCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 教师ID
    course_name = db.Column(db.String(100), nullable=False)  # 课程名称
    classroom = db.Column(db.String(50), nullable=False)  # 上课教室
    class_name = db.Column(db.String(50), nullable=False)  # 上课班级
    semester = db.Column(db.String(20), nullable=False)  # 学期（如：2023-2024-1）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间

    teacher = db.relationship('User', backref=db.backref('courses', lazy=True)) 

class Internship(db.Model):
    """实习管理模型"""
    id = db.Column(db.Integer, primary_key=True)
    # 学院信息
    college = db.Column(db.String(100), nullable=False)  # 学院
    major_name = db.Column(db.String(100), nullable=False)  # 专业名称
    major_type = db.Column(db.String(20))  # 专业性质（师范/非师范）
    
    # 学生基本信息
    class_name = db.Column(db.String(50), nullable=False)  # 班级
    student_id = db.Column(db.String(20), nullable=False)  # 学号
    student_name = db.Column(db.String(50), nullable=False)  # 学生姓名
    student_gender = db.Column(db.String(10))  # 性别
    student_phone = db.Column(db.String(20))  # 联系方式
    
    # 实习信息
    internship_type = db.Column(db.String(20))  # 实习类型（基地/自主）
    start_date = db.Column(db.Date, nullable=False)  # 开始日期
    end_date = db.Column(db.Date, nullable=False)  # 结束日期
    company_name = db.Column(db.String(200), nullable=False)  # 实习单位
    province = db.Column(db.String(50))  # 所属省份
    city = db.Column(db.String(50))  # 所在城市
    detailed_address = db.Column(db.String(200))  # 详细地址
    base_type = db.Column(db.String(20))  # 基地类型（企业/教育）
    
    # 实习评价
    internship_score = db.Column(db.String(20))  # 实习成绩
    is_excellent_intern = db.Column(db.Boolean, default=False)  # 是否优秀实习生
    
    # 关联教师
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 校外指导教师
    external_teacher_name = db.Column(db.String(50))  # 姓名
    external_teacher_position = db.Column(db.String(50))  # 职务
    external_teacher_phone = db.Column(db.String(20))  # 联系方式
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'college': self.college,
            'major_name': self.major_name,
            'major_type': self.major_type,
            'class_name': self.class_name,
            'student_id': self.student_id,
            'student_name': self.student_name,
            'student_gender': self.student_gender,
            'student_phone': self.student_phone,
            'internship_type': self.internship_type,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'company_name': self.company_name,
            'province': self.province,
            'city': self.city,
            'detailed_address': self.detailed_address,
            'base_type': self.base_type,
            'internship_score': self.internship_score,
            'is_excellent_intern': self.is_excellent_intern,
            'external_teacher_name': self.external_teacher_name,
            'external_teacher_position': self.external_teacher_position,
            'external_teacher_phone': self.external_teacher_phone
        } 

class TeachingProject(db.Model):
    """教务处所设立项模型"""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)  # 项目类型：课程建设/教学竞赛/教学成果奖/教学团队/教材建设
    project_name = db.Column(db.String(200), nullable=False)  # 项目名称
    project_level = db.Column(db.String(50))  # 项目级别
    approval_date = db.Column(db.Date)  # 立项时间
    completion_date = db.Column(db.Date)  # 结项时间
    status = db.Column(db.String(20))  # 项目状态
    attachment_path = db.Column(db.String(200))  # 附件路径
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'project_type': self.project_type,
            'project_name': self.project_name,
            'project_level': self.project_level,
            'approval_date': self.approval_date.strftime('%Y-%m-%d') if self.approval_date else None,
            'completion_date': self.completion_date.strftime('%Y-%m-%d') if self.completion_date else None,
            'status': self.status,
            'attachment_path': self.attachment_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class EvaluationProject(db.Model):
    """评估中心所设立项模型"""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)  # 项目类型：校级教改/省级教改/省级教学规划课题/其它
    project_name = db.Column(db.String(200), nullable=False)  # 项目名称
    project_level = db.Column(db.String(50))  # 项目级别
    is_completed = db.Column(db.Boolean, default=False)  # 是否结题
    completion_date = db.Column(db.Date)  # 结题时间
    attachment_path = db.Column(db.String(200))  # 附件路径
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'project_type': self.project_type,
            'project_name': self.project_name,
            'project_level': self.project_level,
            'is_completed': self.is_completed,
            'completion_date': self.completion_date.strftime('%Y-%m-%d') if self.completion_date else None,
            'attachment_path': self.attachment_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class ResearchPaper(db.Model):
    """教研成果-论文模型"""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)  # 论文标题
    journal = db.Column(db.String(100))  # 发表期刊
    publish_date = db.Column(db.Date)  # 发表时间
    authors = db.Column(db.String(200))  # 作者列表
    attachment_path = db.Column(db.String(200))  # 附件路径
    achievement_type = db.Column(db.String(50), nullable=True)  # 成果类型
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'title': self.title,
            'journal': self.journal,
            'publish_date': self.publish_date.strftime('%Y-%m-%d') if self.publish_date else None,
            'authors': self.authors,
            'attachment_path': self.attachment_path,
            'achievement_type': self.achievement_type,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class InnovationProject(db.Model):
    """大学生创新创业项目模型"""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_name = db.Column(db.String(200), nullable=False)  # 项目名称
    project_type = db.Column(db.String(50))  # 项目类型：创新训练/创业训练/创业实践
    project_level = db.Column(db.String(50))  # 项目级别：国家级/省级/校级
    start_date = db.Column(db.Date)  # 立项时间
    end_date = db.Column(db.Date)  # 结项时间
    student_name = db.Column(db.String(100))  # 学生负责人
    student_id = db.Column(db.String(20))  # 学生学号
    team_members = db.Column(db.String(500))  # 团队成员
    funding = db.Column(db.Float)  # 资助金额
    status = db.Column(db.String(20))  # 项目状态：在研/已结题/已终止
    achievement = db.Column(db.Text)  # 项目成果
    attachment_path = db.Column(db.String(200))  # 附件路径
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'project_name': self.project_name,
            'project_type': self.project_type,
            'project_level': self.project_level,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'student_name': self.student_name,
            'student_id': self.student_id,
            'team_members': self.team_members,
            'funding': self.funding,
            'status': self.status,
            'achievement': self.achievement,
            'attachment_path': self.attachment_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Competition(db.Model):
    """学科竞赛模型"""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    competition_name = db.Column(db.String(200), nullable=False)  # 竞赛名称
    competition_level = db.Column(db.String(50))  # 竞赛级别：国家级/省级/校级
    award_level = db.Column(db.String(50))  # 获奖等级：特等奖/一等奖/二等奖/三等奖
    competition_date = db.Column(db.Date)  # 获奖时间
    student_name = db.Column(db.String(100))  # 学生负责人
    student_id = db.Column(db.String(20))  # 学生学号
    team_members = db.Column(db.String(500))  # 团队成员
    work_name = db.Column(db.String(200))  # 参赛作品名称
    organizer = db.Column(db.String(200))  # 主办单位
    attachment_path = db.Column(db.String(200))  # 附件路径
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'competition_name': self.competition_name,
            'competition_level': self.competition_level,
            'award_level': self.award_level,
            'competition_date': self.competition_date.strftime('%Y-%m-%d') if self.competition_date else None,
            'student_name': self.student_name,
            'student_id': self.student_id,
            'team_members': self.team_members,
            'work_name': self.work_name,
            'organizer': self.organizer,
            'attachment_path': self.attachment_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class CollegeEvent(db.Model):
    """学院大事记模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    attachment_path = db.Column(db.String(200))
    original_filename = db.Column(db.String(200))  # 添加原始文件名字段
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref=db.backref('college_events', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'event_date': self.event_date.strftime('%Y-%m-%d') if self.event_date else None,
            'description': self.description,
            'attachment_path': self.attachment_path,
            'original_filename': self.original_filename,
            'created_by': self.created_by,
            'creator_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class FiveOneMentor(db.Model):
    """五业导师指导记录模型"""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 指导教师ID
    student_name = db.Column(db.String(50), nullable=False)  # 学生姓名
    student_id = db.Column(db.String(20), nullable=False)  # 学号
    class_name = db.Column(db.String(50), nullable=False)  # 班级
    photo_path = db.Column(db.String(200))  # 学生照片路径
    status = db.Column(db.String(20), default='pending')  # 状态：pending/approved/rejected
    review_comment = db.Column(db.Text)  # 审核意见
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 审核人ID
    review_date = db.Column(db.DateTime)  # 审核日期
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    teacher = db.relationship('User', foreign_keys=[teacher_id], backref=db.backref('mentor_records', lazy=True))
    reviewer = db.relationship('User', foreign_keys=[reviewer_id])

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.name if self.teacher else None,
            'student_name': self.student_name,
            'student_id': self.student_id,
            'class_name': self.class_name,
            'photo_path': self.photo_path,
            'status': self.status,
            'review_comment': self.review_comment,
            'reviewer_id': self.reviewer_id,
            'reviewer_name': self.reviewer.name if self.reviewer else None,
            'review_date': self.review_date.strftime('%Y-%m-%d %H:%M:%S') if self.review_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 

class File(db.Model):
    """文件模型"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('files', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'upload_date': self.upload_date.strftime('%Y-%m-%d %H:%M:%S') if self.upload_date else None,
            'user_id': self.user_id
        } 

class FiveOneProject(db.Model):
    """五个一工程模型"""
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    teacher = db.relationship('User', backref='five_one_projects')
    book_records = db.relationship('BookRecord', backref='project', cascade='all, delete-orphan')
    teaching_records = db.relationship('TeachingRecord', backref='project', cascade='all, delete-orphan')
    research_records = db.relationship('ResearchRecord', backref='project', cascade='all, delete-orphan')
    competition_records = db.relationship('CompetitionRecord', backref='project', cascade='all, delete-orphan')
    training_records = db.relationship('TrainingRecord', backref='project', cascade='all, delete-orphan')

class BookRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('five_one_project.id'), nullable=False)
    book_title = db.Column(db.String(200), nullable=False)
    book_number = db.Column(db.String(50))
    publish_date = db.Column(db.Date)
    publisher = db.Column(db.String(100))
    author = db.Column(db.String(100))
    has_notes = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'book_title': self.book_title,
            'book_number': self.book_number,
            'publish_date': self.publish_date.strftime('%Y-%m-%d %H:%M:%S') if self.publish_date else None,
            'publisher': self.publisher,
            'author': self.author,
            'has_notes': self.has_notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }

class TeachingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('five_one_project.id'), nullable=False)
    achievement_name = db.Column(db.String(200), nullable=False)
    achievement_type = db.Column(db.String(50))
    achievement_date = db.Column(db.Date)
    achievement_ranking = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'achievement_name': self.achievement_name,
            'achievement_type': self.achievement_type,
            'achievement_date': self.achievement_date,
            'achievement_ranking': self.achievement_ranking,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }

class ResearchRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('five_one_project.id'), nullable=False)
    achievement_name = db.Column(db.String(200), nullable=False)
    research_type = db.Column(db.String(50))
    research_date = db.Column(db.Date)
    research_ranking = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'achievement_name': self.achievement_name,
            'research_type': self.research_type,
            'research_date': self.research_date.strftime('%Y-%m-%d %H:%M:%S') if self.research_date else None,
            'research_ranking': self.research_ranking,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }

class CompetitionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('five_one_project.id'), nullable=False)
    competition_name = db.Column(db.String(200), nullable=False)
    competition_organizer = db.Column(db.String(100))
    competition_type = db.Column(db.String(50))
    competition_date = db.Column(db.Date)
    award_level = db.Column(db.String(50))
    student_names = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'competition_name': self.competition_name,
            'competition_organizer': self.competition_organizer,
            'competition_type': self.competition_type,
            'competition_date': self.competition_date.strftime('%Y-%m-%d %H:%M:%S') if self.competition_date else None,
            'award_level': self.award_level,
            'student_names': self.student_names,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }

class TrainingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('five_one_project.id'), nullable=False)
    training_name = db.Column(db.String(200), nullable=False)
    training_organizer = db.Column(db.String(100))
    training_date = db.Column(db.Date)
    training_location = db.Column(db.String(100))
    training_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'training_name': self.training_name,
            'training_organizer': self.training_organizer,
            'training_date': self.training_date.strftime('%Y-%m-%d %H:%M:%S') if self.training_date else None,
            'training_location': self.training_location,
            'training_description': self.training_description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }

class Teacher(db.Model):
    """教师信息模型"""
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)  # 工号
    name = db.Column(db.String(80), nullable=False)  # 姓名
    gender = db.Column(db.String(10))  # 性别
    birth_date = db.Column(db.Date)  # 出生日期
    education = db.Column(db.String(50))  # 学历
    title = db.Column(db.String(50))  # 职称
    department = db.Column(db.String(100))  # 所属系部
    dual_teacher_type = db.Column(db.String(50))  # 双师类型
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date.strftime('%Y-%m-%d') if self.birth_date else None,
            'education': self.education,
            'title': self.title,
            'department': self.department,
            'dual_teacher_type': self.dual_teacher_type,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class Course(db.Model):
    """课程信息模型"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True)  # 课程代码
    course_name = db.Column(db.String(100), nullable=False)  # 课程名称
    credit = db.Column(db.Float)  # 学分
    hours = db.Column(db.Integer)  # 学时
    course_type = db.Column(db.String(50))  # 课程类型（必修/选修）
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 授课教师ID
    classroom = db.Column(db.String(50))  # 教室
    class_name = db.Column(db.String(50))  # 班级
    semester = db.Column(db.String(20))  # 学期
    description = db.Column(db.Text)  # 课程描述
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teacher = db.relationship('User', backref=db.backref('teaching_courses', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'course_code': self.course_code,
            'course_name': self.course_name,
            'credit': self.credit,
            'hours': self.hours,
            'course_type': self.course_type,
            'teacher_id': self.teacher_id,
            'classroom': self.classroom,
            'class_name': self.class_name,
            'semester': self.semester,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 

class ScientificProject(db.Model):
    """科研立项模型"""
    __tablename__ = 'scientific_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_name = db.Column(db.String(200), nullable=False)  # 项目名称
    project_type = db.Column(db.String(50))  # 项目类型
    project_level = db.Column(db.String(50))  # 项目级别
    approval_date = db.Column(db.Date)  # 立项时间
    completion_date = db.Column(db.Date)  # 结项时间
    funding = db.Column(db.Float)  # 经费
    status = db.Column(db.String(20))  # 项目状态：在研/已结题
    
    # 文件路径
    approval_doc = db.Column(db.String(200))  # 立项文件
    notice_doc = db.Column(db.String(200))  # 通知书
    completion_cert = db.Column(db.String(200))  # 结题证书
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    teacher = db.relationship('User', backref=db.backref('scientific_projects', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'project_name': self.project_name,
            'project_type': self.project_type,
            'project_level': self.project_level,
            'approval_date': self.approval_date.strftime('%Y-%m-%d') if self.approval_date else None,
            'completion_date': self.completion_date.strftime('%Y-%m-%d') if self.completion_date else None,
            'funding': self.funding,
            'status': self.status,
            'approval_doc': self.approval_doc,
            'notice_doc': self.notice_doc,
            'completion_cert': self.completion_cert,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 

class PersonalProfile(db.Model):
    __tablename__ = 'personal_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    # 基本信息
    name = db.Column(db.String(80))
    employee_number = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    ethnicity = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    id_number = db.Column(db.String(18))
    political_status = db.Column(db.String(50))
    party_branch = db.Column(db.String(100))
    hometown = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    # 教育背景
    education_level = db.Column(db.String(50))
    degree = db.Column(db.String(50))
    education_date = db.Column(db.Date)
    degree_date = db.Column(db.Date)
    bachelor_school = db.Column(db.String(100))
    master_school = db.Column(db.String(100))
    phd_school = db.Column(db.String(100))
    # 工作信息
    research_direction = db.Column(db.String(200))
    work_start_date = db.Column(db.Date)
    career_start_date = db.Column(db.Date)
    highest_title = db.Column(db.String(50))
    highest_title_date = db.Column(db.Date)
    position = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    department = db.Column(db.String(100))
    # 头像
    photo_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        def safe_str(val):
            if val is None:
                return ""
            try:
                return str(int(float(val)))
            except Exception:
                return str(val)
        if 'phone' in data and data['phone'] is not None:
            data['phone'] = safe_str(data['phone'])
        if 'id_number' in data and data['id_number'] is not None:
            data['id_number'] = safe_str(data['id_number'])
        return data

class ScientificAchievement(db.Model):
    __tablename__ = 'scientific_achievements'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_type = db.Column(db.String(50))  # 成果类型：论文/专利/著作/其它
    title = db.Column(db.String(200), nullable=False)  # 成果名称
    publish_date = db.Column(db.Date)
    description = db.Column(db.Text)
    attachment_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'achievement_type': self.achievement_type,
            'title': self.title,
            'publish_date': self.publish_date.strftime('%Y-%m-%d') if self.publish_date else None,
            'description': self.description,
            'attachment_path': self.attachment_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class ScientificAward(db.Model):
    __tablename__ = 'scientific_awards'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    award_name = db.Column(db.String(200), nullable=False)  # 奖励名称
    award_level = db.Column(db.String(50))  # 奖励级别
    award_date = db.Column(db.Date)
    awarding_body = db.Column(db.String(100))  # 授奖单位
    description = db.Column(db.Text)
    attachment_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'award_name': self.award_name,
            'award_level': self.award_level,
            'award_date': self.award_date.strftime('%Y-%m-%d') if self.award_date else None,
            'awarding_body': self.awarding_body,
            'description': self.description,
            'attachment_path': self.attachment_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 