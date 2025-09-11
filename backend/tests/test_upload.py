import unittest
import os
import tempfile
from app import app, db, User
from werkzeug.datastructures import FileStorage

class UploadTestCase(unittest.TestCase):
    def setUp(self):
        """测试前的设置"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['UPLOAD_FOLDER'] = 'test_uploads'
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # 创建测试上传目录
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
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
        
        # 创建临时测试文件
        self.test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        self.test_file.write(b'Test content')
        self.test_file.close()
        
        self.large_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        self.large_file.write(b'Large content' * 1000)  # 创建一个大文件
        self.large_file.close()

    def tearDown(self):
        """测试后的清理"""
        # 删除测试上传目录及其内容
        import shutil
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
        
        # 删除临时文件
        os.unlink(self.test_file.name)
        os.unlink(self.large_file.name)
        
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_file_upload(self):
        """测试文件上传功能"""
        # 登录用户
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'test123'
        })
        
        # 创建测试文件
        test_file = FileStorage(
            stream=open(self.test_file.name, 'rb'),
            filename='test.txt',
            content_type='text/plain'
        )
        
        # 测试上传
        response = self.client.post('/upload', data={
            'file': test_file
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # 验证文件是否已上传
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test.txt')
        self.assertTrue(os.path.exists(uploaded_file_path))

    def test_invalid_file_upload(self):
        """测试无效文件上传"""
        # 登录用户
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'test123'
        })
        
        # 测试上传空文件
        response = self.client.post('/upload', data={}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('没有选择文件', response_text)
        
        # 测试上传超大文件
        large_file = FileStorage(
            stream=open(self.large_file.name, 'rb'),
            filename='large.txt',
            content_type='text/plain'
        )
        response = self.client.post('/upload', data={
            'file': large_file
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('文件大小超过限制', response_text)

    def test_file_download(self):
        """测试文件下载功能"""
        # 登录用户
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'test123'
        })
        
        # 上传测试文件
        test_file = FileStorage(
            stream=open(self.test_file.name, 'rb'),
            filename='test.txt',
            content_type='text/plain'
        )
        self.client.post('/upload', data={
            'file': test_file
        })
        
        # 测试下载
        response = self.client.get('/download/test.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/plain')
        
        # 测试下载不存在的文件
        response = self.client.get('/download/nonexistent.txt')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 