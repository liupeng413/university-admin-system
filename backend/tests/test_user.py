import unittest
from app import app, db, User
from flask_login import login_user

class UserTestCase(unittest.TestCase):
    def setUp(self):
        """测试前的设置"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # 创建数据库
        db.create_all()
        
        # 创建测试用户
        self.admin_user = User(
            username='admin',
            name='管理员',
            role='admin'
        )
        self.admin_user.set_password('admin123')
        
        self.teacher_user = User(
            username='teacher',
            name='测试教师',
            role='teacher'
        )
        self.teacher_user.set_password('teacher123')
        
        db.session.add(self.admin_user)
        db.session.add(self.teacher_user)
        db.session.commit()

    def tearDown(self):
        """测试后的清理"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_login(self):
        """测试用户登录功能"""
        # 测试管理员登录
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # 测试教师登录
        response = self.client.post('/login', data={
            'username': 'teacher',
            'password': 'teacher123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # 测试错误密码
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('用户名或密码错误', response_text)

    def test_user_registration(self):
        """测试用户注册功能"""
        # 登录管理员
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        # 测试注册新用户
        response = self.client.post('/register', data={
            'username': 'newuser',
            'name': '新用户',
            'password': 'newpass123',
            'role': 'teacher'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # 验证用户是否创建成功
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, '新用户')
        self.assertEqual(user.role, 'teacher')

    def test_user_permissions(self):
        """测试用户权限控制"""
        # 登录管理员
        with self.client:
            self.client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            })
            
            # 测试管理员权限
            response = self.client.get('/admin')
            self.assertEqual(response.status_code, 200)
            
            # 测试教师权限
            response = self.client.get('/teacher')
            self.assertEqual(response.status_code, 200)

        # 登录教师
        with self.client:
            self.client.post('/login', data={
                'username': 'teacher',
                'password': 'teacher123'
            })
            
            # 测试教师权限
            response = self.client.get('/teacher')
            self.assertEqual(response.status_code, 200)
            
            # 测试访问管理员页面
            response = self.client.get('/admin')
            self.assertEqual(response.status_code, 403)  # 应该被禁止访问

if __name__ == '__main__':
    unittest.main() 