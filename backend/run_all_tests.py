import unittest
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入所有测试用例
from tests.test_user import UserTestCase
from tests.test_five_one import FiveOneTestCase
from tests.test_upload import UploadTestCase
from tests.test_db import DatabaseTestCase

def run_tests():
    """运行所有测试用例"""
    # 创建测试加载器
    loader = unittest.TestLoader()
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试用例
    test_suite.addTests(loader.loadTestsFromTestCase(UserTestCase))
    test_suite.addTests(loader.loadTestsFromTestCase(FiveOneTestCase))
    test_suite.addTests(loader.loadTestsFromTestCase(UploadTestCase))
    test_suite.addTests(loader.loadTestsFromTestCase(DatabaseTestCase))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 根据测试结果设置退出码
    sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
    run_tests() 