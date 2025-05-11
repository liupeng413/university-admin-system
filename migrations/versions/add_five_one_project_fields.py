"""add fields to five_one_project table

Revision ID: add_five_one_project_fields
Revises: 
Create Date: 2024-03-13

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # 添加新字段到 five_one_project 表
    op.add_column('five_one_project', sa.Column('book_number', sa.String(50)))
    op.add_column('five_one_project', sa.Column('publish_date', sa.Date))
    op.add_column('five_one_project', sa.Column('publisher', sa.String(100)))
    op.add_column('five_one_project', sa.Column('author', sa.String(100)))
    op.add_column('five_one_project', sa.Column('has_notes', sa.Boolean, default=False))
    
    op.add_column('five_one_project', sa.Column('teaching_achievement_name', sa.String(255)))
    op.add_column('five_one_project', sa.Column('achievement_type', sa.String(50)))
    op.add_column('five_one_project', sa.Column('achievement_date', sa.Date))
    op.add_column('five_one_project', sa.Column('achievement_ranking', sa.String(50)))
    
    op.add_column('five_one_project', sa.Column('research_achievement_name', sa.String(255)))
    op.add_column('five_one_project', sa.Column('research_type', sa.String(50)))
    op.add_column('five_one_project', sa.Column('research_date', sa.Date))
    op.add_column('five_one_project', sa.Column('research_ranking', sa.String(50)))
    
    op.add_column('five_one_project', sa.Column('competition_name', sa.String(255)))
    op.add_column('five_one_project', sa.Column('competition_organizer', sa.String(100)))
    op.add_column('five_one_project', sa.Column('competition_type', sa.String(50)))
    op.add_column('five_one_project', sa.Column('competition_date', sa.Date))
    op.add_column('five_one_project', sa.Column('award_level', sa.String(50)))
    op.add_column('five_one_project', sa.Column('student_names', sa.String(500)))
    
    op.add_column('five_one_project', sa.Column('training_name', sa.String(255)))
    op.add_column('five_one_project', sa.Column('training_organizer', sa.String(100)))
    op.add_column('five_one_project', sa.Column('training_date', sa.Date))
    op.add_column('five_one_project', sa.Column('training_location', sa.String(100)))
    op.add_column('five_one_project', sa.Column('training_description', sa.Text))
    
    op.add_column('five_one_project', sa.Column('created_at', sa.DateTime, default=sa.func.now()))
    op.add_column('five_one_project', sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()))

def downgrade():
    # 删除添加的字段
    columns = [
        'book_number', 'publish_date', 'publisher', 'author', 'has_notes',
        'teaching_achievement_name', 'achievement_type', 'achievement_date', 'achievement_ranking',
        'research_achievement_name', 'research_type', 'research_date', 'research_ranking',
        'competition_name', 'competition_organizer', 'competition_type', 'competition_date',
        'award_level', 'student_names',
        'training_name', 'training_organizer', 'training_date', 'training_location',
        'training_description', 'created_at', 'updated_at'
    ]
    
    for column in columns:
        op.drop_column('five_one_project', column) 