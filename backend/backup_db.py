import os
import shutil
from datetime import datetime

def backup_database():
    """备份数据库文件"""
    # 源数据库文件
    source_db = 'university.db'
    
    # 如果数据库文件存在
    if os.path.exists(source_db):
        # 创建备份目录
        backup_dir = 'db_backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # 生成备份文件名（包含时间戳）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'university_{timestamp}.db')
        
        # 复制数据库文件
        shutil.copy2(source_db, backup_file)
        print(f"数据库已备份到: {backup_file}")
    else:
        print("数据库文件不存在")

if __name__ == '__main__':
    backup_database() 