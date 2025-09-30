from app import db

# 删除已存在的表（如果存在）
db.engine.execute('DROP TABLE IF EXISTS five_one_project')

# 创建新表
sql = '''
CREATE TABLE five_one_project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    book_title TEXT,
    book_number TEXT,
    publish_date DATE,
    publisher TEXT,
    author TEXT,
    has_notes BOOLEAN DEFAULT 0,
    teaching_achievement_name TEXT,
    achievement_type TEXT,
    achievement_date DATE,
    achievement_ranking TEXT,
    research_achievement_name TEXT,
    research_type TEXT,
    research_date DATE,
    research_ranking TEXT,
    competition_name TEXT,
    competition_organizer TEXT,
    competition_type TEXT,
    competition_date DATE,
    award_level TEXT,
    student_names TEXT,
    training_name TEXT,
    training_organizer TEXT,
    training_date DATE,
    training_location TEXT,
    training_description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(teacher_id) REFERENCES user(id)
)
'''

db.engine.execute(sql)
print("表创建成功！") 