from app import app, db
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_teacher_data():
    with app.app_context():
        try:
            # 获取所有教师用户
            teachers = User.query.filter_by(role='teacher').all()
            logger.info(f"Found {len(teachers)} teachers to update")

            for teacher in teachers:
                # 如果name字段存储的是密码hash，则需要修复
                if len(teacher.name or '') > 50 and '$' in (teacher.name or ''):
                    # 将密码hash移动到正确的字段
                    teacher.password_hash = teacher.name
                    teacher.name = None  # 清空错误的name字段
                
                # 确保is_dual_teacher是布尔值
                if isinstance(teacher.is_dual_teacher, str):
                    teacher.is_dual_teacher = teacher.is_dual_teacher.lower() == 'true'
                
                # 如果birth_date是None，设置一个默认值或保持为None
                if teacher.birth_date is None:
                    logger.warning(f"Teacher {teacher.username} has no birth_date")
                
                # 确保所有必需字段都有值
                if not teacher.role:
                    teacher.role = 'teacher'
                
            db.session.commit()
            logger.info("Successfully updated teacher data")
            
        except Exception as e:
            logger.error(f"Error updating teacher data: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    update_teacher_data() 