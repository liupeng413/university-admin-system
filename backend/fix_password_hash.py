from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_password_hashes():
    with app.app_context():
        try:
            # 获取所有用户
            users = User.query.all()
            logger.info(f"找到 {len(users)} 个用户需要更新")

            for user in users:
                # 检查是否是scrypt哈希
                if user.password_hash and 'scrypt' in user.password_hash:
                    # 重置为默认密码123456，使用pbkdf2:sha256算法
                    user.password_hash = generate_password_hash('123456', method='pbkdf2:sha256')
                    logger.info(f"已重置用户 {user.username} 的密码为默认密码")
            
            db.session.commit()
            logger.info("成功更新所有用户的密码哈希")
            
        except Exception as e:
            logger.error(f"更新密码哈希时出错: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    fix_password_hashes() 