#!/bin/bash

# 数据库文件和备份目录
DB_FILE="$(dirname "$0")/backend/university.db"
BACKUP_DIR="$(dirname "$0")/db_backup"
BACKUP_FILE="$BACKUP_DIR/university_backup.db"

# 创建备份目录（如果不存在）
mkdir -p "$BACKUP_DIR"

# 删除旧的备份文件（只保留一个）
rm -f "$BACKUP_FILE"

# 复制数据库文件为备份
cp "$DB_FILE" "$BACKUP_FILE"

# 输出日志
NOW=$(date '+%Y-%m-%d %H:%M:%S')
echo "$NOW 数据库备份完成，备份文件：$BACKUP_FILE" 