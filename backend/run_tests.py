import unittest
import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入测试用例
from tests.test_five_one import FiveOneTestCase

if __name__ == '__main__':
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(FiveOneTestCase)
    
    # 运行测试
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # 根据测试结果设置退出码
    sys.exit(not result.wasSuccessful()) 