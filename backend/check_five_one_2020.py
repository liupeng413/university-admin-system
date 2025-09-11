from app import app, db
from models import FiveOneProject, BookRecord, TeachingRecord, ResearchRecord, CompetitionRecord, TrainingRecord

with app.app_context():
    projects = FiveOneProject.query.filter_by(year=2020).all()
    if not projects:
        print('未找到2020年五个一工程数据')
    for project in projects:
        print(f'五个一工程ID: {project.id}, 教师ID: {project.teacher_id}, 年份: {project.year}')
        print('  一本书:')
        for book in project.book_records:
            print('   ', {c.name: getattr(book, c.name) for c in book.__table__.columns})
        print('  教研成果:')
        for rec in project.teaching_records:
            print('   ', {c.name: getattr(rec, c.name) for c in rec.__table__.columns})
        print('  科研成果:')
        for rec in project.research_records:
            print('   ', {c.name: getattr(rec, c.name) for c in rec.__table__.columns})
        print('  竞赛:')
        for rec in project.competition_records:
            print('   ', {c.name: getattr(rec, c.name) for c in rec.__table__.columns})
        print('  培训:')
        for rec in project.training_records:
            print('   ', {c.name: getattr(rec, c.name) for c in rec.__table__.columns}) 