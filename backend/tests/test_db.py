import unittest
from app import app, db, User, FiveOneProject
from datetime import datetime

class DatabaseTestCase(unittest.TestCase):
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
        self.user = User(
            username='testuser',
            name='测试用户',
            role='teacher'
        )
        self.user.set_password('test123')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """测试后的清理"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        """测试用户创建"""
        # 创建新用户
        new_user = User(
            username='newuser',
            name='新用户',
            role='teacher'
        )
        new_user.set_password('newpass123')
        db.session.add(new_user)
        db.session.commit()
        
        # 验证用户是否创建成功
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, '新用户')
        self.assertEqual(user.role, 'teacher')

    def test_five_one_project_creation(self):
        """测试五个一工程记录创建"""
        # 创建五个一工程记录
        project = FiveOneProject(
            year=2023,
            teacher_id=self.user.id,
            book_title='测试图书',
            book_number='ISBN123456',
            publish_date=datetime.strptime('2023-01-01', '%Y-%m-%d'),
            publisher='测试出版社',
            author='测试作者',
            has_notes=True,
            teaching_achievement_name='测试教研成果',
            achievement_type='论文',
            achievement_date=datetime.strptime('2023-02-01', '%Y-%m-%d'),
            achievement_ranking='第一',
            research_achievement_name='测试科研成果',
            research_type='项目',
            research_date=datetime.strptime('2023-03-01', '%Y-%m-%d'),
            research_ranking='主持人',
            competition_name='测试竞赛',
            competition_organizer='测试单位',
            competition_type='专业竞赛',
            competition_date=datetime.strptime('2023-04-01', '%Y-%m-%d'),
            award_level='一等奖',
            student_names='张三,李四',
            training_name='测试培训',
            training_organizer='培训机构',
            training_date=datetime.strptime('2023-05-01', '%Y-%m-%d'),
            training_location='培训地点',
            training_description='培训内容描述'
        )
        db.session.add(project)
        db.session.commit()
        
        # 验证记录是否创建成功
        saved_project = FiveOneProject.query.filter_by(
            teacher_id=self.user.id,
            year=2023
        ).first()
        self.assertIsNotNone(saved_project)
        self.assertEqual(saved_project.book_title, '测试图书')
        self.assertEqual(saved_project.award_level, '一等奖')

    def test_data_relationships(self):
        """测试数据关系"""
        # 创建五个一工程记录
        project = FiveOneProject(
            year=2023,
            teacher_id=self.user.id,
            book_title='测试图书'
        )
        db.session.add(project)
        db.session.commit()
        
        # 验证用户和项目的关系
        user_projects = self.user.five_one_projects
        self.assertEqual(len(user_projects), 1)
        self.assertEqual(user_projects[0].book_title, '测试图书')

    def test_data_deletion(self):
        """测试数据删除"""
        # 创建测试数据
        project = FiveOneProject(
            year=2023,
            teacher_id=self.user.id,
            book_title='测试图书'
        )
        db.session.add(project)
        db.session.commit()
        
        # 删除数据
        db.session.delete(project)
        db.session.commit()
        
        # 验证数据是否已删除
        deleted_project = FiveOneProject.query.filter_by(
            teacher_id=self.user.id,
            year=2023
        ).first()
        self.assertIsNone(deleted_project)

if __name__ == '__main__':
    unittest.main() 