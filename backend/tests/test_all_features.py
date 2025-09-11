import unittest
from datetime import datetime
import os
import sys
import json

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取backend目录的路径
backend_dir = os.path.dirname(current_dir)
# 将backend目录添加到Python路径
sys.path.insert(0, backend_dir)

from app import app, db, User, FiveOneProject, TeacherCourse, TeachingProject, ResearchPaper, InnovationProject, Competition, CollegeEvent, FiveOneMentor
from flask_login import login_user

class AllFeaturesTestCase(unittest.TestCase):
    def setUp(self):
        """测试前设置"""
        # 创建测试数据库
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        # 确保应用上下文
        self.app_context = app.app_context()
        self.app_context.push()
        
        # 清理并重新创建所有表
        db.drop_all()
        db.create_all()
        
        # 创建测试用户
        self.normal_user = User(username='test_user', name='测试用户', role='teacher')
        self.normal_user.set_password('test_password')
        db.session.add(self.normal_user)
        
        self.special_user1 = User(username='special_user1', name='张艳鹏', role='teacher')
        self.special_user1.set_password('test_password')
        db.session.add(self.special_user1)
        
        self.special_user2 = User(username='special_user2', name='王鹏', role='teacher')
        self.special_user2.set_password('test_password')
        db.session.add(self.special_user2)
        
        db.session.commit()
        
        # 存储用户ID供后续使用
        self.normal_user_id = self.normal_user.id
        self.special_user1_id = self.special_user1.id
        self.special_user2_id = self.special_user2.id
        
        # 创建测试客户端
        self.client = app.test_client()
        
        # 登录普通用户
        with self.client:
            self.client.post('/login', data={
                'username': 'test_user',
                'password': 'test_password'
            })

    def tearDown(self):
        """测试后清理"""
        # 清理数据库会话
        db.session.remove()
        
        # 删除测试数据库
        db.drop_all()
        
        # 移除应用上下文
        self.app_context.pop()
        
        # 删除测试数据库文件
        if os.path.exists('test.db'):
            os.remove('test.db')

    def login(self, username, password):
        """辅助登录函数"""
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def test_profile(self):
        """测试个人信息功能"""
        # 查看个人信息页面
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('个人信息', response_text)
        
        # 修改个人信息
        new_data = {
            'name': '新测试用户',
            'role': 'teacher'
        }
        response = self.client.post('/profile', data=new_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # 验证修改结果
        response = self.client.get('/profile')
        response_text = response.data.decode('utf-8')
        self.assertIn('新测试用户', response_text)

    def test_change_password(self):
        """测试修改密码功能"""
        # 修改密码
        new_data = {
            'password': 'new_password',
            'confirm_password': 'new_password'
        }
        response = self.client.post('/change_password', data=new_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # 使用新密码登录
        self.login('test_user', 'new_password')
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)

    def test_teacher_teaching(self):
        """测试常规教学功能"""
        # 添加课程
        new_course = {
            'course_name': '测试课程',
            'classroom': 'A101',
            'class_name': '测试班级',
            'semester': '2024-1'
        }
        response = self.client.post('/api/teacher/courses', data=new_course)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        if data is None:
            print("Response data is None")
            print("Response content:", response.data.decode('utf-8'))
        self.assertTrue(data.get('success', False))
        
        # 查看课程列表
        response = self.client.get('/teacher_teaching')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('测试课程', response_text)

    def test_teaching_research(self):
        """测试教学立项与教研成果功能"""
        # 添加教学立项
        new_project = {
            'project_type': '课程建设',
            'project_name': '测试教学项目',
            'project_level': '校级',
            'approval_date': '2024-01-01',
            'completion_date': '2024-12-31',
            'status': '在研'
        }
        response = self.client.post('/api/teaching_projects', data=new_project)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        if data is None:
            print("Response data is None")
            print("Response content:", response.data.decode('utf-8'))
        self.assertTrue(data.get('success', False))
        
        # 查看教学立项列表
        response = self.client.get('/teaching_research')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('测试教学项目', response_text)

    def test_innovation_achievements(self):
        """测试双创成果功能"""
        # 添加双创项目
        new_project = {
            'project_name': '测试双创项目',
            'project_type': '创新训练',
            'project_level': '校级',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'student_name': '测试学生',
            'student_id': '2024001',
            'team_members': '成员1,成员2',
            'funding': '5000',
            'status': '在研'
        }
        response = self.client.post('/api/innovation_projects', data=new_project)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        if data is None:
            print("Response data is None")
            print("Response content:", response.data.decode('utf-8'))
        self.assertTrue(data.get('success', False))
        
        # 查看双创项目列表
        response = self.client.get('/innovation_achievements')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('测试双创项目', response_text)

    def test_scientific_research(self):
        """测试科研立项与成果功能"""
        # 添加科研论文
        new_paper = {
            'title': '测试科研论文',
            'journal': '测试期刊',
            'publish_date': '2024-01-01',
            'authors': '作者1,作者2'
        }
        response = self.client.post('/api/research_papers', data=new_paper)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        if data is None:
            print("Response data is None")
            print("Response content:", response.data.decode('utf-8'))
        self.assertTrue(data.get('success', False))
        
        # 查看科研论文列表
        response = self.client.get('/scientific_research')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('测试科研论文', response_text)

    def test_five_one_mentor(self):
        """测试五业导师功能"""
        # 添加导师记录
        new_record = {
            'student_name': '测试学生',
            'student_id': '2024001',
            'class_name': '测试班级'
        }
        response = self.client.post('/api/five_one_mentor/records', data=new_record)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        if data is None:
            print("Response data is None")
            print("Response content:", response.data.decode('utf-8'))
        self.assertTrue(data.get('success', False))
        
        # 查看导师记录列表
        response = self.client.get('/five_one_mentor')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('测试学生', response_text)

    def test_college_events(self):
        """测试学院大事记功能"""
        # 添加大事记
        new_event = {
            'title': '测试大事记',
            'event_date': '2024-01-01',
            'description': '测试描述'
        }
        response = self.client.post('/api/college_events', data=new_event)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        if data is None:
            print("Response data is None")
            print("Response content:", response.data.decode('utf-8'))
        self.assertTrue(data.get('success', False))
        
        # 查看大事记列表
        response = self.client.get('/college_events')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('测试大事记', response_text)

    def test_special_user_permissions(self):
        """测试特殊用户权限"""
        # 登录特殊用户1（张艳鹏）
        self.login('special_user1', 'test_password')
        
        # 测试查看所有教师的五个一工程
        response = self.client.get('/view_five_one/2020')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('五个一工程汇总', response_text)
        
        # 测试查看所有教师的常规教学
        response = self.client.get('/teacher_teaching')
        self.assertEqual(response.status_code, 200)
        
        # 登录特殊用户2（王鹏）
        self.login('special_user2', 'test_password')
        
        # 测试查看所有教师的科研立项
        response = self.client.get('/scientific_research')
        self.assertEqual(response.status_code, 200)
        
        # 测试查看所有教师的双创成果
        response = self.client.get('/innovation_achievements')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main() 