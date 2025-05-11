-- 创新创业项目表
CREATE TABLE IF NOT EXISTS innovation_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    project_name TEXT NOT NULL,
    project_type TEXT NOT NULL,
    project_level TEXT NOT NULL,
    funding DECIMAL(10,2),
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    team_members TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    status TEXT NOT NULL,
    achievement TEXT,
    attachment_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES user(id)
);

-- 学科竞赛表
CREATE TABLE IF NOT EXISTS competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    competition_name TEXT NOT NULL,
    competition_level TEXT NOT NULL,
    award_level TEXT NOT NULL,
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    team_members TEXT,
    work_name TEXT NOT NULL,
    competition_date DATE NOT NULL,
    organizer TEXT NOT NULL,
    attachment_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES user(id)
);

-- 学院大事记表
CREATE TABLE IF NOT EXISTS college_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    event_date DATE NOT NULL,
    description TEXT NOT NULL,
    attachment_path TEXT,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES user(id)
); 