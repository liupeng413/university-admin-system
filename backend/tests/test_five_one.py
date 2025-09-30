import unittest
from datetime import datetime
from app import app, db, User, FiveOneProject
from flask_login import login_user
import os

class FiveOneTestCase(unittest.TestCase):
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
        
        self.special_user = User(username='special_user', name='张艳鹏', role='teacher')
        self.special_user.set_password('test_password')
        db.session.add(self.special_user)
        
        db.session.commit()
        
        # 存储用户ID供后续使用
        self.normal_user_id = self.normal_user.id
        self.special_user_id = self.special_user.id
        
        # 创建测试数据
        self.test_project = FiveOneProject(
            year=2020,
            teacher_id=self.normal_user_id,
            book_title='测试图书',
            publisher='测试出版社',
            publish_date=datetime.strptime('2020-01-01', '%Y-%m-%d').date(),
            author='测试作者',
            has_notes=True,
            teaching_achievement_name='测试论文',
            achievement_type='论文',
            achievement_date=datetime.strptime('2020-02-01', '%Y-%m-%d').date(),
            achievement_ranking='第一作者',
            research_achievement_name='测试项目',
            research_type='项目',
            research_date=datetime.strptime('2020-03-01', '%Y-%m-%d').date(),
            research_ranking='主持人',
            competition_name='测试竞赛',
            competition_organizer='测试单位',
            competition_type='测试类型',
            competition_date=datetime.strptime('2020-04-01', '%Y-%m-%d').date(),
            award_level='一等奖',
            student_names='测试学生',
            training_name='测试培训',
            training_organizer='测试机构',
            training_date=datetime.strptime('2020-05-01', '%Y-%m-%d').date(),
            training_location='测试地点',
            training_description='测试描述'
        )
        db.session.add(self.test_project)
        db.session.commit()
        
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

    def test_normal_user_view(self):
        """测试普通用户查看功能"""
        # 测试查看自己的记录
        response = self.client.get('/api/five_one/2020')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['book_title'], '测试图书')
        
        # 测试查看不存在的年份
        response = self.client.get('/api/five_one/2022')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data['success'])

    def test_special_user_view(self):
        """测试特殊用户查看功能"""
        # 先登录特殊用户
        self.login('special_user', 'test_password')
        
        # 测试查看所有记录
        response = self.client.get('/api/five_one/2020')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(isinstance(data['data'], list))
        self.assertEqual(len(data['data']), 1)  # 应该有一条记录
        
        # 测试查看特定教师的记录
        response = self.client.get(f'/api/five_one/2020?teacher_id={self.normal_user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['book_title'], '测试图书')

    def test_save_five_one(self):
        """测试保存功能"""
        # 测试保存新记录
        new_data = {
            'year': '2024',
            'book_title': '新图书',
            'book_number': 'ISBN123456',
            'publisher': '新出版社',
            'publish_date': '2024-01-01',
            'author': '新作者',
            'has_notes': 'true',
            'teaching_achievement_name': '新教研成果',
            'achievement_type': '论文',
            'achievement_date': '2024-02-01',
            'achievement_ranking': '第一作者',
            'research_achievement_name': '新科研成果',
            'research_type': '项目',
            'research_date': '2024-03-01',
            'research_ranking': '主持人',
            'competition_name': '新竞赛',
            'competition_organizer': '新单位',
            'competition_type': '新类型',
            'competition_date': '2024-04-01',
            'award_level': '特等奖',
            'student_names': '小明,小红',
            'training_name': '新培训',
            'training_organizer': '新机构',
            'training_date': '2024-05-01',
            'training_location': '新地点',
            'training_description': '新描述'
        }
        
        response = self.client.post('/save_five_one', data=new_data)
        self.assertEqual(response.status_code, 302)  # 应该重定向
        
        # 验证保存的数据
        response = self.client.get('/api/five_one/2024')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['book_title'], '新图书')

    def test_view_five_one_page(self):
        """测试查看页面"""
        # 测试查看所有记录的页面
        response = self.client.get('/view_five_one/2020')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('五个一工程 - 2020年', response_text)
        
        # 测试查看特定教师的记录页面
        response = self.client.get(f'/view_five_one/2020?teacher_id={self.normal_user_id}')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('测试图书', response_text)

if __name__ == '__main__':
    unittest.main() 