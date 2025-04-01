from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(80))
    role = db.Column(db.String(20))  # admin或teacher
    title = db.Column(db.String(50))  # 职称
    major = db.Column(db.String(50))  # 学科类别
    research_direction = db.Column(db.String(200))  # 研究方向
    address = db.Column(db.String(200))  # 家庭住址
    phone = db.Column(db.String(20))  # 联系电话
    hometown = db.Column(db.String(100))  # 籍贯
    employee_number = db.Column(db.Integer, default=0)  # 工号

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'role': self.role,
            'title': self.title,
            'major': self.major,
            'research_direction': self.research_direction,
            'address': self.address,
            'phone': self.phone,
            'hometown': self.hometown,
            'employee_number': self.employee_number
        } 