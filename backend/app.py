import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
import uuid
from collections import defaultdict
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from backend.models import User, db, Internship, GraduationProject, TeacherCourse, TeachingProject, EvaluationProject, ResearchPaper, InnovationProject, Competition, CollegeEvent, FiveOneMentor, File, FiveOneProject, Teacher, Course, ScientificProject, ScientificAward, BookRecord, TeachingRecord, ResearchRecord, CompetitionRecord, TrainingRecord
import subprocess
import shutil
import platform
import time


def get_file_extension(filename):
    """获取文件扩展名"""
    return os.path.splitext(filename)[1] if filename else ''

def save_uploaded_file(file, upload_folder):
    """保存上传的文件
    Args:
        file: FileStorage对象
        upload_folder: 上传目录路径
    Returns:
        tuple: (是否成功, 保存的文件名或错误信息, 错误代码)
        错误代码：0-成功，1-文件已存在，2-其他错误
    """
    if not file:
        return False, "没有文件被上传", 2
    
    original_filename = file.filename
    file_path = os.path.join(upload_folder, original_filename)
    
    # 检查文件是否已存在
    if os.path.exists(file_path):
        return False, "文件已存在", 1
        
    try:
        file.save(file_path)
        return True, original_filename, 0
    except Exception as e:
        return False, str(e), 2

app = Flask(__name__, 
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)
app.config['SECRET_KEY'] = 'your-fixed-secret-key-here'  # 使用固定的密钥
app.config['WTF_CSRF_SECRET_KEY'] = 'your-fixed-csrf-secret-key-here'  # 使用固定的CSRF密钥
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 会话持续时间为24小时
app.config['SESSION_COOKIE_SECURE'] = False  # 允许HTTP
app.config['SESSION_COOKIE_HTTPONLY'] = True  # 防止JavaScript访问cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # 防止CSRF攻击
app.config['WTF_CSRF_ENABLED'] = True  # 启用CSRF保护
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # CSRF令牌有效期1小时
app.config['PREFERRED_URL_SCHEME'] = 'http'  # 设置首选URL方案为HTTP
csrf = CSRFProtect(app)

# 配置数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'university.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db.init_app(app)
migrate = Migrate(app, db)  # 初始化Flask-Migrate
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            print(f"尝试登录 - 用户名: {username}, 密码: {password}")
            
            user = User.query.filter_by(username=username).first()
            if user:
                print(f"找到用户: {user.username}, 角色: {user.role}")
                if user.check_password(password):
                    print("密码验证成功")
                    login_user(user, remember=True)  # 设置remember=True
                    session.permanent = True  # 设置会话为永久性
                    # 将用户信息存储在session中
                    session['user_info'] = user.to_dict()
                    # 生成新的CSRF令牌
                    csrf_token = csrf._get_csrf_token()
                    response = redirect(url_for('profile'))
                    response.set_cookie('csrf_token', csrf_token)
                    return response
                else:
                    print("密码验证失败")
            else:
                print(f"未找到用户: {username}")
            
            flash('用户名或密码错误')
        except Exception as e:
            print(f"登录出错: {str(e)}")
            flash('登录失败：' + str(e))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # 从session中获取用户信息
    user_info = session.get('user_info', {})
    return render_template('dashboard.html', user_info=user_info)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        try:
            # 处理头像上传
            if 'photo' in request.files and request.files['photo'].filename:
                photo = request.files['photo']
                # 检查文件类型，确保只允许上传图片文件
                if not allowed_file(photo.filename):
                    return 'File type not allowed', 400
                # 确保文件名安全
                filename = secure_filename(photo.filename)
                # 强制指定文件后缀为 .jpg
                unique_filename = f"{current_user.id}_{int(time.time())}.jpg"
                # 保存文件
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], 'avatars', unique_filename)
                os.makedirs(os.path.dirname(photo_path), exist_ok=True)
                photo.save(photo_path)
                # 更新数据库中的头像路径
                current_user.photo_path = f"avatars/{unique_filename}"

            # 处理基本信息
            current_user.name = request.form.get('name') or None
            current_user.employee_number = request.form.get('employee_number') or None
            current_user.gender = request.form.get('gender') or None
            current_user.ethnicity = request.form.get('ethnicity') or None
            current_user.id_number = request.form.get('id_number') or None
            current_user.political_status = request.form.get('political_status') or None
            current_user.hometown = request.form.get('hometown') or None
            current_user.phone = request.form.get('phone') or None
            current_user.email = request.form.get('email') or None
            current_user.address = request.form.get('address') or None

            # 处理教育背景
            current_user.education_level = request.form.get('education_level') or None
            current_user.degree = request.form.get('degree') or None
            current_user.bachelor_school = request.form.get('bachelor_school') or None
            current_user.master_school = request.form.get('master_school') or None
            current_user.phd_school = request.form.get('phd_school') or None

            # 处理工作信息
            current_user.major = request.form.get('major') or None
            current_user.teaching_group = request.form.get('teaching_group') or None
            current_user.is_dual_teacher = request.form.get('is_dual_teacher') or None
            current_user.award_title = request.form.get('award_title') or None
            current_user.talent_title = request.form.get('talent_title') or None
            current_user.research_direction = request.form.get('research_direction') or None
            current_user.highest_title = request.form.get('highest_title') or None
            current_user.position = request.form.get('position') or None
            current_user.subject = request.form.get('subject') or None
            
            # 处理日期字段
            def parse_date(date_str):
                if date_str and date_str.strip():
                    try:
                        return datetime.strptime(date_str, '%Y-%m-%d').date()
                    except ValueError:
                        return None
                return None

            current_user.birth_date = parse_date(request.form.get('birth_date'))
            current_user.party_join_date = parse_date(request.form.get('party_join_date'))
            current_user.education_date = parse_date(request.form.get('education_date'))
            current_user.degree_date = parse_date(request.form.get('degree_date'))
            current_user.work_start_date = parse_date(request.form.get('work_start_date'))
            current_user.career_start_date = parse_date(request.form.get('career_start_date'))
            current_user.highest_title_date = parse_date(request.form.get('highest_title_date'))

            # 处理政治面貌相关字段
            current_user.political_status = request.form.get('political_status') or None
            current_user.party_branch = request.form.get('party_branch') if request.form.get('political_status') == '中共党员' else None

            # 提交更改
            db.session.commit()
            
            # 根据请求类型返回响应
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': '个人信息更新成功！',
                    'data': current_user.to_dict()
                })
            else:
                flash('个人信息更新成功！')
                return redirect(url_for('profile'))
                
        except Exception as e:
            db.session.rollback()
            error_message = f'更新失败：{str(e)}'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': error_message
                }), 500
            else:
                flash(error_message, 'error')
                return redirect(url_for('profile'))

    return render_template('profile.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('没有选择文件')
        return redirect(url_for('dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('没有选择文件')
        return redirect(url_for('dashboard'))
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_file = File(
            filename=filename,
            original_filename=file.filename,
            upload_date=datetime.utcnow(),
            user_id=current_user.id
        )
        db.session.add(new_file)
        db.session.commit()
        
        flash('文件上传成功')
    return redirect(url_for('dashboard'))

@app.route('/download/<path:filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/teachers')
@login_required
def teachers():
    if current_user.role != 'admin':
        flash('您没有权限访问该页面')
        return redirect(url_for('profile'))
    
    # 获取筛选参数
    major = request.args.get('major')
    highest_title = request.args.get('highest_title')
    
    # 构建查询
    query = User.query.filter_by(role='teacher')
    
    # 应用筛选条件
    if major:
        query = query.filter_by(major=major)
    if highest_title:
        query = query.filter_by(highest_title=highest_title)
    
    # 获取筛选后的教师列表
    teachers = query.all()
    return render_template('teachers.html', teachers=teachers)

@app.route('/teacher/<int:id>')
@login_required
def view_teacher(id):
    if current_user.role != 'admin':
        flash('您没有权限访问该页面')
        return redirect(url_for('profile'))
    
    teacher = User.query.get_or_404(id)
    return render_template('teacher_detail.html', teacher=teacher)

@app.route('/teacher/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    if current_user.role != 'admin':
        flash('您没有权限访问该页面')
        return redirect(url_for('profile'))
    
    teacher = User.query.get_or_404(id)
    if request.method == 'POST':
        try:
            # 更新教师信息
            teacher.name = request.form.get('name')
            teacher.gender = request.form.get('gender')
            teacher.ethnicity = request.form.get('ethnicity')
            teacher.political_status = request.form.get('political_status')
            teacher.employee_number = request.form.get('employee_number')
            
            # 处理日期字段
            birth_date = request.form.get('birth_date')
            if birth_date:
                teacher.birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
            
            work_start_date = request.form.get('work_start_date')
            if work_start_date:
                teacher.work_start_date = datetime.strptime(work_start_date, '%Y-%m-%d')
            
            # 更新其他字段
            teacher.major = request.form.get('major')
            teacher.title = request.form.get('title')
            teacher.teaching_group = request.form.get('teaching_group')
            
            db.session.commit()
            flash('教师信息更新成功！')
            return redirect(url_for('view_teacher', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash('更新失败：' + str(e))
            
    return render_template('edit_teacher.html', teacher=teacher)

# 定义有效的职称列表
VALID_TITLES = ['教授', '副教授', '讲师', '助教']

@app.route('/teacher/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_teacher_old(id):
    teacher = User.query.get_or_404(id)
    if current_user.role != 'admin' and current_user.id != id:
        flash('您没有权限编辑此教师信息')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            # 只有管理员可以修改工号
            if current_user.role == 'admin':
                employee_number = request.form.get('employee_number', type=int)
                if employee_number is not None:
                    teacher.employee_number = employee_number

            # 验证职称
            title = request.form.get('title')
            if title not in VALID_TITLES:
                flash('无效的职称选择')
                return redirect(url_for('edit_teacher', id=id))

            # 添加日志
            print("正在保存教师信息...")
            print(f"身份证号: {request.form.get('id_number')}")

            teacher.name = request.form.get('name')
            teacher.gender = request.form.get('gender')
            teacher.ethnicity = request.form.get('ethnicity')
            teacher.birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date()
            teacher.hometown = request.form.get('hometown')
            teacher.id_number = request.form.get('id_number')
            teacher.political_status = request.form.get('political_status')
            teacher.party_join_date = datetime.strptime(request.form.get('party_join_date'), '%Y-%m-%d').date()
            teacher.major = request.form.get('major')
            teacher.title = title
            teacher.position = request.form.get('position')
            teacher.department = request.form.get('department')
            teacher.address = request.form.get('address')
            teacher.phone = request.form.get('phone')
            teacher.email = request.form.get('email')
            teacher.bachelor_school = request.form.get('bachelor_school')
            teacher.master_school = request.form.get('master_school')
            teacher.phd_school = request.form.get('phd_school')
            teacher.research_direction = request.form.get('research_direction')
            teacher.work_start_date = datetime.strptime(request.form.get('work_start_date'), '%Y-%m-%d').date()

            db.session.commit()
            flash('教师信息更新成功')
            return redirect(url_for('view_teacher', id=id))
        except Exception as e:
            flash('更新失败：' + str(e))
            return redirect(url_for('edit_teacher', id=id))

    return render_template('edit_teacher.html', teacher=teacher)

@app.route('/files')
@login_required
def list_files():
    if current_user.role == 'admin':
        # 管理员可以看到所有文件
        files = File.query.all()
    else:
        # 普通用户只能看到自己的文件
        files = current_user.files
    return render_template('files.html', files=files)

@app.route('/delete_file/<filename>', methods=['DELETE'])
@login_required
def delete_file(filename):
    file = File.query.filter_by(filename=filename).first_or_404()
    
    # 检查权限：只有文件所有者或管理员可以删除文件
    if current_user.role != 'admin' and file.user_id != current_user.id:
        return '没有权限删除此文件', 403
    
    try:
        # 删除物理文件
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 删除数据库记录
        db.session.delete(file)
        db.session.commit()
        return '文件删除成功', 200
    except Exception as e:
        db.session.rollback()
        return '文件删除失败：' + str(e), 500

@app.route('/teacher_statistics')
@login_required
def teacher_statistics():
    # 获取所有教师信息（如果是特定用户）
    teachers = []
    if current_user.username in ['zhangyanpeng', 'wangpeng']:
        teachers = Teacher.query.all()
    
    return render_template('teacher_statistics.html', teachers=teachers)

@app.route('/api/teacher/details/<employee_id>')
@login_required
def get_teacher_details(employee_id):
    # 检查用户权限
    if current_user.username not in ['zhangyanpeng', 'wangpeng']:
        return jsonify({'success': False, 'error': '没有权限访问此信息'})
    
    teacher = Teacher.query.filter_by(employee_id=employee_id).first()
    if not teacher:
        return jsonify({'success': False, 'error': '未找到教师信息'})
    
    return jsonify({
        'success': True,
        'data': {
            'employee_id': teacher.employee_id,
            'name': teacher.name,
            'gender': teacher.gender,
            'birth_date': teacher.birth_date.strftime('%Y-%m-%d') if teacher.birth_date else '',
            'education': teacher.education,
            'title': teacher.title,
            'department': teacher.department,
            'dual_teacher_type': teacher.dual_teacher_type
        }
    })

@app.route('/api/teachers/<int:id>', methods=['PUT'])
@login_required
def update_teacher(id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': '没有权限进行此操作'}), 403
    
    teacher = User.query.get_or_404(id)
    data = request.get_json()
    
    if 'employee_number' in data:
        teacher.employee_number = data['employee_number']
        
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/teachers')
@login_required
def get_teachers():
    teachers = User.query.filter_by(role='teacher').all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'gender': t.gender,
        'ethnicity': t.ethnicity,
        'birth_date': t.birth_date.strftime('%Y-%m-%d') if t.birth_date else None,
        'work_start_date': t.work_start_date.strftime('%Y-%m-%d') if t.work_start_date else None,
        'major': t.major,
        'title': t.title,
        'research_direction': t.research_direction,
        'address': t.address,
        'phone': t.phone,
        'employee_number': t.employee_number
    } for t in teachers])

@app.route('/api/user/role')
@login_required
def get_user_role():
    return jsonify({'role': current_user.role})

@app.route('/teacher/<int:id>/update_employee_number', methods=['POST'])
@login_required
def update_employee_number(id):
    if current_user.role != 'admin':
        flash('只有管理员可以修改工号')
        return redirect(url_for('teachers'))
    
    teacher = User.query.get_or_404(id)
    employee_number = request.form.get('employee_number', type=int)
    
    if employee_number is not None:
        teacher.employee_number = employee_number
        try:
            db.session.commit()
            flash('工号更新成功')
        except Exception as e:
            db.session.rollback()
            flash('工号更新失败：' + str(e))
    else:
        flash('无效的工号')
    
    return redirect(url_for('teachers'))

@app.route('/upload_photo', methods=['POST'])
@login_required
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        # 生成唯一的文件名
        filename = secure_filename(f"{current_user.id}_{file.filename}")
        # 确保上传目录存在
        upload_folder = os.path.join(app.root_path, 'static', 'uploads', 'photos')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        
        # 保存文件
        file.save(filepath)
        
        # 更新用户照片路径
        current_user.photo_path = f"uploads/photos/{filename}"
        db.session.commit()
        
        return jsonify({'success': True, 'photo_path': current_user.photo_path})
    
    return jsonify({'error': '不支持的文件类型'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """修改密码"""
    data = request.get_json()
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    
    if not password or not confirm_password:
        return jsonify({'success': False, 'error': '密码不能为空'})
        
    if password != confirm_password:
        return jsonify({'success': False, 'error': '两次输入的密码不一致'})
    
    try:
        current_user.set_password(password)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/teacher_stats')
@login_required
@admin_required
def teacher_stats():
    # 获取教师总数
    total_teachers = User.query.filter_by(role='teacher').count()
    
    # 按学历统计
    education_stats = db.session.query(
        User.education_level,
        func.count(User.id)
    ).filter_by(role='teacher').group_by(User.education_level).all()
    
    # 按职称统计
    title_stats = db.session.query(
        User.highest_title,
        func.count(User.id)
    ).filter_by(role='teacher').group_by(User.highest_title).all()
    
    # 按性别统计
    gender_stats = db.session.query(
        User.gender,
        func.count(User.id)
    ).filter_by(role='teacher').group_by(User.gender).all()
    
    # 按双师统计
    dual_teacher_stats = db.session.query(
        User.is_dual_teacher,
        func.count(User.id)
    ).filter_by(role='teacher').group_by(User.is_dual_teacher).all()
    
    # 按年龄段统计
    age_stats = {
        '35岁以下': 0,
        '36-45岁': 0,
        '46-55岁': 0,
        '56岁以上': 0
    }
    
    teachers = User.query.filter_by(role='teacher').all()
    for teacher in teachers:
        if teacher.age:
            if teacher.age <= 35:
                age_stats['35岁以下'] += 1
            elif teacher.age <= 45:
                age_stats['36-45岁'] += 1
            elif teacher.age <= 55:
                age_stats['46-55岁'] += 1
            else:
                age_stats['56岁以上'] += 1
    
    return render_template('teacher_stats.html',
                         total_teachers=total_teachers,
                         education_stats=education_stats,
                         title_stats=title_stats,
                         gender_stats=gender_stats,
                         dual_teacher_stats=dual_teacher_stats,
                         age_stats=age_stats)

@app.route('/all_teachers')
@login_required
@admin_required
def all_teachers():
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('all_teachers.html', teachers=teachers)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/photo/<path:filename>')
def get_photo(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        # 如果找不到上传的头像，返回默认头像
        if 'avatars/' in filename:  # 如果是请求头像
            user = User.query.filter_by(photo_path=filename).first()
            if user and user.gender:
                if user.gender == '男':
                    return send_from_directory(app.static_folder, 'img/boy.png')
                elif user.gender == '女':
                    return send_from_directory(app.static_folder, 'img/girl.png')
            return send_from_directory(app.static_folder, 'img/boy.png')
        abort(404)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('您没有权限访问该页面')
        return redirect(url_for('profile'))
    return render_template('admin_dashboard.html')

@app.route('/five_one')
@login_required
def five_one():
    # 渲染五个一工程页面
    return render_template('five_one.html')

@app.route('/api/teacher_stats')
@login_required
def get_teacher_stats():
    if current_user.username not in ['zhangyanpeng', 'wangpeng']:
        return jsonify({'error': '无权限访问'}), 403

    # 获取所有教师数据
    teachers = User.query.all()

    # 年龄结构统计
    age_stats = {}
    for teacher in teachers:
        if teacher.birth_date:
            age = (datetime.now().year - teacher.birth_date.year)
            age_range = f"{age//10*10}-{age//10*10+9}岁"
            age_stats[age_range] = age_stats.get(age_range, 0) + 1

    # 对年龄结构数据进行排序
    sorted_age_stats = dict(sorted(age_stats.items(), key=lambda x: int(x[0].split('-')[0])))

    # 学历结构统计
    education_stats = {}
    for teacher in teachers:
        if teacher.education_level:
            education_stats[teacher.education_level] = education_stats.get(teacher.education_level, 0) + 1

    # 职称结构统计
    title_stats = {}
    for teacher in teachers:
        if teacher.highest_title:
            title_stats[teacher.highest_title] = title_stats.get(teacher.highest_title, 0) + 1

    # 双师结构统计
    dual_teacher_stats = {'是': 0, '否': 0}
    for teacher in teachers:
        if teacher.is_dual_teacher:
            dual_teacher_stats[teacher.is_dual_teacher] += 1

    # 性别结构统计
    gender_stats = {'男': 0, '女': 0}
    for teacher in teachers:
        if teacher.gender:
            gender_stats[teacher.gender] += 1

    return jsonify({
        'age_labels': list(sorted_age_stats.keys()),
        'age_data': list(sorted_age_stats.values()),
        'education_labels': list(education_stats.keys()),
        'education_data': list(education_stats.values()),
        'title_labels': list(title_stats.keys()),
        'title_data': list(title_stats.values()),
        'dual_teacher_data': [dual_teacher_stats['是'], dual_teacher_stats['否']],
        'gender_data': [gender_stats['男'], gender_stats['女']]
    })

@app.route('/save_five_one', methods=['POST'])
@login_required
def save_five_one():
    try:
        year = request.form.get('year')
        if not year:
            flash('请选择年份', 'error')
            return redirect(url_for('five_one'))

        # 一本书
        book_titles = request.form.getlist('book_title[]')
        book_numbers = request.form.getlist('book_number[]')
        publish_dates = request.form.getlist('publish_date[]')
        publishers = request.form.getlist('publisher[]')
        authors = request.form.getlist('author[]')
        has_notes_list = request.form.getlist('has_notes[]')
        # 教研成果
        teaching_names = request.form.getlist('teaching_achievement_name[]')
        achievement_types = request.form.getlist('achievement_type[]')
        achievement_dates = request.form.getlist('achievement_date[]')
        achievement_rankings = request.form.getlist('achievement_ranking[]')
        # 科研成果
        research_names = request.form.getlist('research_achievement_name[]')
        research_types = request.form.getlist('research_type[]')
        research_dates = request.form.getlist('research_date[]')
        research_rankings = request.form.getlist('research_ranking[]')
        # 竞赛
        competition_names = request.form.getlist('competition_name[]')
        competition_organizers = request.form.getlist('competition_organizer[]')
        competition_types = request.form.getlist('competition_type[]')
        competition_dates = request.form.getlist('competition_date[]')
        award_levels = request.form.getlist('award_level[]')
        student_names_list = request.form.getlist('student_names[]')
        # 培训
        training_names = request.form.getlist('training_name[]')
        training_organizers = request.form.getlist('training_organizer[]')
        training_dates = request.form.getlist('training_date[]')
        training_locations = request.form.getlist('training_location[]')
        training_descriptions = request.form.getlist('training_description[]')

        # 校验每一项：只要有一项填写就必须全部填写
        for i in range(len(book_titles)):
            if book_titles[i] or book_numbers[i] or publish_dates[i] or publishers[i] or authors[i]:
                if not (book_titles[i] and book_numbers[i] and publish_dates[i] and publishers[i] and authors[i]):
                    flash('请完整填写每本书的所有字段', 'error')
                    return redirect(url_for('five_one'))
        for i in range(len(teaching_names)):
            if teaching_names[i] or achievement_types[i] or achievement_dates[i] or achievement_rankings[i]:
                if not (teaching_names[i] and achievement_types[i] and achievement_dates[i] and achievement_rankings[i]):
                    flash('请完整填写每项教研成果的所有字段', 'error')
                    return redirect(url_for('five_one'))
        for i in range(len(research_names)):
            if research_names[i] or research_types[i] or research_dates[i] or research_rankings[i]:
                if not (research_names[i] and research_types[i] and research_dates[i] and research_rankings[i]):
                    flash('请完整填写每项科研成果的所有字段', 'error')
                    return redirect(url_for('five_one'))
        for i in range(len(competition_names)):
            if competition_names[i] or competition_organizers[i] or competition_types[i] or competition_dates[i] or award_levels[i] or student_names_list[i]:
                if not (competition_names[i] and competition_organizers[i] and competition_types[i] and competition_dates[i] and award_levels[i] and student_names_list[i]):
                    flash('请完整填写每项竞赛的所有字段', 'error')
                    return redirect(url_for('five_one'))
        for i in range(len(training_names)):
            if training_names[i] or training_organizers[i] or training_dates[i] or training_locations[i] or training_descriptions[i]:
                if not (training_names[i] and training_organizers[i] and training_dates[i] and training_locations[i] and training_descriptions[i]):
                    flash('请完整填写每项培训的所有字段', 'error')
                    return redirect(url_for('five_one'))

        # 查找或创建 FiveOneProject
        project = FiveOneProject.query.filter_by(year=year, teacher_id=current_user.id).first()
        if not project:
            project = FiveOneProject(year=year, teacher_id=current_user.id)
            db.session.add(project)
            db.session.flush()  # 获取project.id

        # 删除原有子记录
        BookRecord.query.filter_by(project_id=project.id).delete()
        TeachingRecord.query.filter_by(project_id=project.id).delete()
        ResearchRecord.query.filter_by(project_id=project.id).delete()
        CompetitionRecord.query.filter_by(project_id=project.id).delete()
        TrainingRecord.query.filter_by(project_id=project.id).delete()

        # 一本书
        for i in range(len(book_titles)):
            if book_titles[i] and book_numbers[i] and publish_dates[i] and publishers[i] and authors[i]:
                db.session.add(BookRecord(
                    project_id=project.id,
                    book_title=book_titles[i],
                    book_number=book_numbers[i],
                    publish_date=datetime.strptime(publish_dates[i], '%Y-%m-%d'),
                    publisher=publishers[i],
                    author=authors[i],
                    has_notes=(has_notes_list[i] == 'true')
                ))
        # 教研成果
        for i in range(len(teaching_names)):
            if teaching_names[i] and achievement_types[i] and achievement_dates[i] and achievement_rankings[i]:
                db.session.add(TeachingRecord(
                    project_id=project.id,
                    achievement_name=teaching_names[i],
                    achievement_type=achievement_types[i],
                    achievement_date=datetime.strptime(achievement_dates[i], '%Y-%m-%d'),
                    achievement_ranking=achievement_rankings[i]
                ))
        # 科研成果
        for i in range(len(research_names)):
            if research_names[i] and research_types[i] and research_dates[i] and research_rankings[i]:
                db.session.add(ResearchRecord(
                    project_id=project.id,
                    achievement_name=research_names[i],
                    research_type=research_types[i],
                    research_date=datetime.strptime(research_dates[i], '%Y-%m-%d'),
                    research_ranking=research_rankings[i]
                ))
        # 竞赛
        for i in range(len(competition_names)):
            if competition_names[i] and competition_organizers[i] and competition_types[i] and competition_dates[i] and award_levels[i] and student_names_list[i]:
                db.session.add(CompetitionRecord(
                    project_id=project.id,
                    competition_name=competition_names[i],
                    competition_organizer=competition_organizers[i],
                    competition_type=competition_types[i],
                    competition_date=datetime.strptime(competition_dates[i], '%Y-%m-%d'),
                    award_level=award_levels[i],
                    student_names=student_names_list[i]
                ))
        # 培训
        for i in range(len(training_names)):
            if training_names[i] and training_organizers[i] and training_dates[i] and training_locations[i] and training_descriptions[i]:
                db.session.add(TrainingRecord(
                    project_id=project.id,
                    training_name=training_names[i],
                    training_organizer=training_organizers[i],
                    training_date=datetime.strptime(training_dates[i], '%Y-%m-%d'),
                    training_location=training_locations[i],
                    training_description=training_descriptions[i]
                ))

        db.session.commit()
        flash('信息保存成功', 'success')
        return redirect(url_for('five_one'))
    except Exception as e:
        db.session.rollback()
        flash(f'保存失败：{str(e)}', 'error')
        return redirect(url_for('five_one'))

def can_view_all_five_one():
    """检查当前用户是否有权限查看所有教师的五个一工程信息"""
    special_users = ['张艳鹏', '王鹏']
    return current_user.name in special_users

@app.route('/api/five_one/<int:year>', methods=['GET'])
@login_required
def get_five_one_by_year(year):
    try:
        # 转换year为整数以确保类型匹配
        year = int(year)
        
        # 如果是特殊用户，需要传入教师ID来查询特定教师的记录
        teacher_id = request.args.get('teacher_id', type=int)
        
        if can_view_all_five_one():
            if teacher_id:
                # 如果提供了teacher_id，查询特定教师的记录
                project = FiveOneProject.query.filter_by(
                    year=year,
                    teacher_id=teacher_id
                ).first()
                teacher = User.query.get(teacher_id)
                teacher_name = teacher.name if teacher else "未知教师"
            else:
                # 如果没有提供teacher_id，返回所有教师的记录列表
                projects = FiveOneProject.query.filter_by(year=year).all()
                return jsonify({
                    'success': True,
                    'data': [{
                        'teacher_id': project.teacher_id,
                        'teacher_name': User.query.get(project.teacher_id).name,
                        'book_records': [record.to_dict() for record in project.book_records],
                        'teaching_records': [record.to_dict() for record in project.teaching_records],
                        'research_records': [record.to_dict() for record in project.research_records],
                        'competition_records': [record.to_dict() for record in project.competition_records],
                        'training_records': [record.to_dict() for record in project.training_records]
                    } for project in projects]
                })
        else:
            # 普通用户只能查看自己的记录
            project = FiveOneProject.query.filter_by(
                year=year,
                teacher_id=current_user.id
            ).first()
            teacher_name = current_user.name

        if not project:
            return jsonify({
                'success': False,
                'message': f'{teacher_name}还未编辑{year}年信息'
            })
            
        return jsonify({
            'success': True,
            'data': {
                'teacher_id': project.teacher_id,
                'teacher_name': teacher_name,
                'book_records': [record.to_dict() for record in project.book_records],
                'teaching_records': [record.to_dict() for record in project.teaching_records],
                'research_records': [record.to_dict() for record in project.research_records],
                'competition_records': [record.to_dict() for record in project.competition_records],
                'training_records': [record.to_dict() for record in project.training_records]
            }
        })
    except Exception as e:
        print(f"Error in get_five_one_by_year: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取数据时发生错误：{str(e)}'
        })

@app.route('/api/five_one/records/<record_type>', methods=['POST'])
@login_required
def add_five_one_record(record_type):
    try:
        year = request.form.get('year')
        if not year:
            return jsonify({'success': False, 'message': '请选择年份'})

        # 获取或创建项目记录
        project = FiveOneProject.query.filter_by(
            year=year,
            teacher_id=current_user.id
        ).first()
        
        if not project:
            project = FiveOneProject(year=year, teacher_id=current_user.id)
            db.session.add(project)
            db.session.flush()  # 获取project.id

        # 根据记录类型创建相应的记录
        if record_type == 'book':
            record = BookRecord(
                project_id=project.id,
                book_title=request.form.get('book_title'),
                book_number=request.form.get('book_number'),
                publish_date=datetime.strptime(request.form.get('publish_date'), '%Y-%m-%d').date() if request.form.get('publish_date') else None,
                publisher=request.form.get('publisher'),
                author=request.form.get('author'),
                has_notes=request.form.get('has_notes') == 'true'
            )
        elif record_type == 'teaching':
            record = TeachingRecord(
                project_id=project.id,
                achievement_name=request.form.get('achievement_name'),
                achievement_type=request.form.get('achievement_type'),
                achievement_date=datetime.strptime(request.form.get('achievement_date'), '%Y-%m-%d').date() if request.form.get('achievement_date') else None,
                achievement_ranking=request.form.get('achievement_ranking')
            )
        elif record_type == 'research':
            record = ResearchRecord(
                project_id=project.id,
                achievement_name=request.form.get('achievement_name'),
                research_type=request.form.get('research_type'),
                research_date=datetime.strptime(request.form.get('research_date'), '%Y-%m-%d').date() if request.form.get('research_date') else None,
                research_ranking=request.form.get('research_ranking')
            )
        elif record_type == 'competition':
            record = CompetitionRecord(
                project_id=project.id,
                competition_name=request.form.get('competition_name'),
                competition_organizer=request.form.get('competition_organizer'),
                competition_type=request.form.get('competition_type'),
                competition_date=datetime.strptime(request.form.get('competition_date'), '%Y-%m-%d').date() if request.form.get('competition_date') else None,
                award_level=request.form.get('award_level'),
                student_names=request.form.get('student_names')
            )
        elif record_type == 'training':
            record = TrainingRecord(
                project_id=project.id,
                training_name=request.form.get('training_name'),
                training_organizer=request.form.get('training_organizer'),
                training_date=datetime.strptime(request.form.get('training_date'), '%Y-%m-%d').date() if request.form.get('training_date') else None,
                training_location=request.form.get('training_location'),
                training_description=request.form.get('training_description')
            )
        else:
            return jsonify({'success': False, 'message': '无效的记录类型'})

        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '添加成功',
            'data': record.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'添加失败：{str(e)}'
        })

@app.route('/api/five_one/records/<record_type>/<int:record_id>', methods=['DELETE'])
@login_required
def delete_five_one_record(record_type, record_id):
    try:
        # 根据记录类型获取相应的模型
        model_map = {
            'book': BookRecord,
            'teaching': TeachingRecord,
            'research': ResearchRecord,
            'competition': CompetitionRecord,
            'training': TrainingRecord
        }
        
        if record_type not in model_map:
            return jsonify({'success': False, 'message': '无效的记录类型'})
            
        record = model_map[record_type].query.get_or_404(record_id)
        
        # 检查权限
        if record.project.teacher_id != current_user.id and not can_view_all_five_one():
            return jsonify({'success': False, 'message': '没有权限删除此记录'})
            
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败：{str(e)}'
        })

@app.route('/view_five_one/<int:year>')
@login_required
def view_five_one(year):
    try:
        year = int(year)
        teacher_id = request.args.get('teacher_id', type=int)
        if can_view_all_five_one():
            if teacher_id:
                record = FiveOneProject.query.filter_by(year=year, teacher_id=teacher_id).first()
            else:
                records = FiveOneProject.query.filter_by(year=year).all()
                teachers = {r.teacher_id: User.query.get(r.teacher_id).name for r in records}
                # 组装每个教师的所有五个一工程子项为列表
                record_list = []
                for r in records:
                    record_list.append({
                        'teacher_id': r.teacher_id,
                        'book_records': [b.to_dict() for b in r.book_records],
                        'teaching_records': [t.to_dict() for t in r.teaching_records],
                        'research_records': [t.to_dict() for t in r.research_records],
                        'competition_records': [t.to_dict() for t in r.competition_records],
                        'training_records': [t.to_dict() for t in r.training_records],
                    })
                return render_template('view_five_one_list.html', records=record_list, teachers=teachers, year=year)
        else:
            record = FiveOneProject.query.filter_by(year=year, teacher_id=current_user.id).first()
        if not record:
            teacher_name = User.query.get(teacher_id).name if teacher_id else current_user.name
            flash(f'{teacher_name}还未编辑{year}年信息', 'info')
            return redirect(url_for('five_one'))
        return render_template('view_five_one.html', record=record)
    except Exception as e:
        flash(f'获取数据时发生错误：{str(e)}', 'error')
        return redirect(url_for('five_one'))

@app.route('/graduation_projects')
@login_required
def graduation_projects():
    projects = GraduationProject.query.filter_by(teacher_id=current_user.id).all()
    return render_template('graduation_projects.html', projects=projects)

@app.route('/api/graduation_projects', methods=['GET', 'POST'])
@login_required
def handle_graduation_projects():
    if request.method == 'GET':
        try:
            # 获取查询参数
            student_name = request.args.get('student_name', '')
            teacher_name = request.args.get('teacher_name', '')
            
            # 构建查询
            query = GraduationProject.query
            
            if student_name:
                query = query.filter(GraduationProject.student_name.like(f'%{student_name}%'))
            
            if teacher_name and current_user.role == 'admin':
                teacher = Teacher.query.filter(Teacher.name.like(f'%{teacher_name}%')).first()
                if teacher:
                    query = query.filter_by(teacher_id=teacher.id)
            
            # 如果不是管理员，只显示自己的项目
            if current_user.role != 'admin':
                query = query.filter_by(teacher_id=current_user.id)
            
            projects = query.all()
            return jsonify({
                'success': True,
                'message': '获取成功',
                'data': [project.to_dict() for project in projects]
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取失败：{str(e)}'
            })
    
    elif request.method == 'POST':
        try:
            data = request.form.to_dict()
            
            # 处理附件上传
            file = request.files.get('attachment')
            if file:
                from datetime import datetime
                employee_number = current_user.employee_number
                date_prefix = datetime.now().strftime('%Y-%m-%d')
                filename = f"{date_prefix}_{file.filename}"
                upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'graduation_projects', str(employee_number))
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                data['attachment_path'] = f'graduation_projects/{employee_number}/{filename}'
            
            # 添加教师ID
            data['teacher_id'] = current_user.id
            
            # 创建新项目
            project = GraduationProject(**data)
            db.session.add(project)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': '创建成功',
                'data': project.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'创建失败：{str(e)}'
            })

@app.route('/api/graduation_projects/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def handle_graduation_project(id):
    project = GraduationProject.query.get_or_404(id)
    
    # 检查权限
    if project.teacher_id != current_user.id and current_user.role != 'admin':
        return jsonify({
            'success': False,
            'message': '没有权限操作此项目'
        })
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'message': '获取成功',
            'data': project.to_dict()
        })
    
    elif request.method == 'PUT':
        try:
            data = request.form.to_dict()
            
            # 处理附件上传
            file = request.files.get('attachment')
            if file:
                # 删除旧附件
                if project.attachment_path:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], project.attachment_path))
                    except:
                        pass
                from datetime import datetime
                employee_number = current_user.employee_number
                date_prefix = datetime.now().strftime('%Y-%m-%d')
                filename = f"{date_prefix}_{file.filename}"
                upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'graduation_projects', str(employee_number))
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                data['attachment_path'] = f'graduation_projects/{employee_number}/{filename}'
            
            # 更新项目信息
            for key, value in data.items():
                setattr(project, key, value)
            
            db.session.commit()
            return jsonify({
                'success': True,
                'message': '更新成功',
                'data': project.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'更新失败：{str(e)}'
            })
    
    elif request.method == 'DELETE':
        try:
            # 删除附件
            if project.attachment_path:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], project.attachment_path))
                except:
                    pass
            
            db.session.delete(project)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': '删除成功'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'删除失败：{str(e)}'
            })

@app.route('/api/graduation_projects/stats')
@login_required
def graduation_projects_stats():
    # 获取所有毕业设计记录
    projects = GraduationProject.query.all()
    
    # 按教师姓名和届次统计
    stats = {}
    for project in projects:
        teacher_name = project.teacher.name
        year = project.graduation_year
        
        if teacher_name not in stats:
            stats[teacher_name] = {}
        if year not in stats[teacher_name]:
            stats[teacher_name][year] = {
                'total': 0,
                'excellent': 0,
                'good': 0,
                'medium': 0,
                'pass': 0,
                'fail': 0
            }
        
        # 统计总数
        stats[teacher_name][year]['total'] += 1
        
        # 统计各等级数量
        if project.grade == '优秀':
            stats[teacher_name][year]['excellent'] += 1
        elif project.grade == '良好':
            stats[teacher_name][year]['good'] += 1
        elif project.grade == '中等':
            stats[teacher_name][year]['medium'] += 1
        elif project.grade == '及格':
            stats[teacher_name][year]['pass'] += 1
        elif project.grade == '不及格':
            stats[teacher_name][year]['fail'] += 1
    
    return jsonify(stats)

@app.route('/internships')
@login_required
def internships():
    """显示教师指导的学生实习列表"""
    if current_user.role == 'admin':
        internships = Internship.query.all()
    else:
        internships = Internship.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher_internships.html', internships=internships)

@app.route('/add_internship', methods=['POST'])
@login_required
def add_internship():
    """添加新的实习记录"""
    try:
        # 将字符串 'true'/'false' 转换为布尔值
        is_excellent = request.form['is_excellent'].lower() == 'true'
        
        internship = Internship(
            # 学院信息
            college=request.form['college'],
            major_name=request.form['major_name'],
            major_type=request.form['major_type'],
            
            # 学生基本信息
            class_name=request.form['class_name'],
            student_id=request.form['student_id'],
            student_name=request.form['student_name'],
            student_gender=request.form['student_gender'],
            student_phone=request.form.get('student_phone'),
            
            # 实习评价
            internship_score=request.form['internship_score'],
            is_excellent_intern=is_excellent,
            
            # 实习信息
            internship_type=request.form['internship_type'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
            company_name=request.form['company_name'],
            province=request.form['province'],
            city=request.form['city'],
            detailed_address=request.form['detailed_address'],
            base_type=request.form['base_type'],
            
            # 关联教师
            teacher_id=current_user.id,
            
            # 校外指导教师
            external_teacher_name=request.form['external_teacher_name'],
            external_teacher_position=request.form['external_teacher_position'],
            external_teacher_phone=request.form['external_teacher_phone']
        )
        db.session.add(internship)
        db.session.commit()
        flash('实习记录添加成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'添加失败：{str(e)}', 'error')
    return redirect(url_for('teacher_teaching'))

@app.route('/internship/<int:id>/delete', methods=['POST'])
@login_required
def delete_internship_old(id):
    return redirect(url_for('delete_internship', id=id))

@app.route('/teacher_teaching')
@login_required
def teacher_teaching():
    """显示教师常规教学页面"""
    try:
        # 获取查询参数
        tab = request.args.get('tab', 'graduation')
        student_name = request.args.get('student_name', '')
        teacher_name = request.args.get('teacher_name', '')
        
        # 检查是否为管理员或教务处老师
        is_admin_teacher = current_user.role == 'admin'
        
        # 获取教师的课程信息
        courses = TeacherCourse.query.filter_by(teacher_id=current_user.id).all() if not is_admin_teacher else TeacherCourse.query.all()
        
        # 获取毕业设计信息
        graduation_projects_query = GraduationProject.query
        if not is_admin_teacher:
            graduation_projects_query = graduation_projects_query.filter_by(teacher_id=current_user.id)
        graduation_projects = graduation_projects_query.all()
        
        # 获取实习信息
        internships_query = Internship.query
        if not is_admin_teacher:
            internships_query = internships_query.filter_by(teacher_id=current_user.id)
        internships = internships_query.all()
        
        return render_template('teacher_teaching.html',
                             courses=courses,
                             graduation_projects=graduation_projects,
                             internships=internships,
                             is_admin_teacher=is_admin_teacher)
    except Exception as e:
        flash(f'加载页面时发生错误：{str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/teaching_research')
@login_required
def teaching_research():
    """教学立项与教研成果页面"""
    return render_template('teaching_research.html', 
                         is_admin_teacher=current_user.username in ['zhangyanpeng', 'wangpeng'])

@app.route('/api/teacher/courses', methods=['POST'])
@login_required
def add_course():
    """添加课程"""
    try:
        data = request.get_json()
        course = TeacherCourse(
            teacher_id=current_user.id,
            course_name=data['course_name'],
            classroom=data['classroom'],
            class_name=data['class_name'],
            semester=data['semester']
        )
        db.session.add(course)
        db.session.commit()
        return jsonify({'success': True, 'message': '添加成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teacher/courses/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def handle_teacher_course(id):
    """处理单个课程的GET、PUT和DELETE请求"""
    course = TeacherCourse.query.get_or_404(id)
    
    # 检查权限
    if current_user.role != 'admin' and course.teacher_id != current_user.id:
        return jsonify({
            'success': False,
            'error': '您没有权限操作此课程'
        }), 403
    
    if request.method == 'GET':
        course_dict = {
            'id': course.id,
            'course_name': course.course_name,
            'classroom': course.classroom,
            'class_name': course.class_name,  # 确保这个字段名与前端一致
            'semester': course.semester,
            'teacher_id': course.teacher_id
        }
        return jsonify({
            'success': True,
            'course': course_dict
        })
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            
            # 更新字段
            course.course_name = data.get('course_name', course.course_name)
            course.classroom = data.get('classroom', course.classroom)
            course.class_name = data.get('class_name', course.class_name)
            course.semester = data.get('semester', course.semester)
            
            db.session.commit()
            return jsonify({
                'success': True,
                'message': '更新成功'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': f'更新失败：{str(e)}'
            }), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(course)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': '删除成功'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': f'删除失败：{str(e)}'
            }), 500

@app.route('/api/internships', methods=['GET'])
@login_required
def get_internships():
    """获取实习记录列表"""
    try:
        if current_user.role == 'admin':
            internships = Internship.query.all()
        else:
            internships = Internship.query.filter_by(teacher_id=current_user.id).all()
        return jsonify({
            'success': True,
            'message': '获取成功',
            'data': [internship.to_dict() for internship in internships]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取失败：{str(e)}'
        })

@app.route('/api/internships/<int:id>', methods=['GET'])
@login_required
def get_internship(id):
    """获取单个实习记录"""
    try:
        internship = Internship.query.get_or_404(id)
        if current_user.role != 'admin' and internship.teacher_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '您没有权限查看此记录'
            })
        return jsonify({
            'success': True,
            'message': '获取成功',
            'data': internship.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取失败：{str(e)}'
        })

@app.route('/api/internships', methods=['POST'])
@login_required
def create_internship():
    """创建新的实习记录"""
    try:
        data = request.get_json()
        
        # 处理日期字段
        if 'start_date' in data:
            data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data:
            data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            
        # 处理布尔值字段
        if 'is_excellent_intern' in data:
            data['is_excellent_intern'] = str(data['is_excellent_intern']).lower() == 'true'
            
        # 添加教师ID
        data['teacher_id'] = current_user.id
        
        # 创建实习记录
        internship = Internship(**data)
        db.session.add(internship)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '创建成功',
            'data': internship.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'创建失败：{str(e)}'
        })

@app.route('/api/internships/<int:id>', methods=['PUT'])
@login_required
def update_internship(id):
    """更新实习记录"""
    try:
        internship = Internship.query.get_or_404(id)
        if current_user.role != 'admin' and internship.teacher_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '您没有权限修改此记录'
            })
            
        data = request.get_json()
        
        # 更新日期字段
        if 'start_date' in data:
            data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data:
            data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            
        # 处理布尔值字段
        if 'is_excellent_intern' in data:
            data['is_excellent_intern'] = str(data['is_excellent_intern']).lower() == 'true'
            
        # 更新实习记录字段
        for key, value in data.items():
            if hasattr(internship, key):
                setattr(internship, key, value)
                
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '更新成功',
            'data': internship.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'更新失败：{str(e)}'
        })

@app.route('/api/internships/<int:id>', methods=['DELETE'])
@login_required
def delete_internship(id):
    try:
        internship = Internship.query.get_or_404(id)
        if current_user.role != 'admin' and internship.teacher_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '您没有权限删除此记录'
            })
        
        db.session.delete(internship)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败：{str(e)}'
        })

# 添加模型的to_dict方法
def add_to_dict_methods():
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    TeacherCourse.to_dict = to_dict
    Internship.to_dict = to_dict
    GraduationProject.to_dict = to_dict

# 确保在应用启动时添加to_dict方法
add_to_dict_methods()

@app.route('/api/teaching_projects', methods=['GET', 'POST'])
@login_required
def handle_teaching_projects():
    if request.method == 'GET':
        try:
            projects = TeachingProject.query.filter_by(teacher_id=current_user.id).all()
            return jsonify({
                'success': True,
                'message': '获取成功',
                'data': [project.to_dict() for project in projects]
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取失败：{str(e)}'
            })
    
    elif request.method == 'POST':
        try:
            data = request.form.to_dict()
            file = request.files.get('attachment')
            
            if file:
                employee_number = current_user.employee_number
                date_prefix = datetime.now().strftime('%Y-%m-%d')
                filename = f"{date_prefix}_{file.filename}"
                upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'teaching_projects', str(employee_number))
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                data['attachment_path'] = f'teaching_projects/{employee_number}/{filename}'
            
            # 处理日期字段
            if 'approval_date' in data:
                data['approval_date'] = datetime.strptime(data['approval_date'], '%Y-%m-%d').date()
            if 'completion_date' in data:
                data['completion_date'] = datetime.strptime(data['completion_date'], '%Y-%m-%d').date()
            
            data['teacher_id'] = current_user.id
            project = TeachingProject(**data)
            db.session.add(project)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': '添加成功',
                'data': project.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'添加失败：{str(e)}'
            })

@app.route('/api/evaluation_projects', methods=['GET', 'POST'])
@login_required
def handle_evaluation_projects():
    if request.method == 'GET':
        try:
            projects = EvaluationProject.query.filter_by(teacher_id=current_user.id).all()
            return jsonify({
                'success': True,
                'message': '获取成功',
                'data': [project.to_dict() for project in projects]
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取失败：{str(e)}'
            })
    
    elif request.method == 'POST':
        try:
            data = request.form.to_dict()
            file = request.files.get('attachment')
            
            if file:
                employee_number = current_user.employee_number
                date_prefix = datetime.now().strftime('%Y-%m-%d')
                filename = f"{date_prefix}_{file.filename}"
                upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'evaluation_projects', str(employee_number))
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                data['attachment_path'] = f'evaluation_projects/{employee_number}/{filename}'
            
            # 处理日期字段
            if 'completion_date' in data:
                data['completion_date'] = datetime.strptime(data['completion_date'], '%Y-%m-%d').date()
            
            # 处理布尔值字段
            data['is_completed'] = data.get('is_completed', 'false').lower() == 'true'
            
            data['teacher_id'] = current_user.id
            project = EvaluationProject(**data)
            db.session.add(project)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': '添加成功',
                'data': project.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'添加失败：{str(e)}'
            })

@app.route('/api/research_papers', methods=['GET', 'POST'])
@login_required
def handle_research_papers():
    if request.method == 'GET':
        try:
            papers = ResearchPaper.query.filter_by(teacher_id=current_user.id).all()
            return jsonify({
                'success': True,
                'message': '获取成功',
                'data': [
                    {
                        'id': paper.id,
                        'title': paper.title,
                        'achievement_name': paper.title,  # 兼容
                        'journal': paper.journal,
                        'description': paper.journal,     # 兼容
                        'publish_date': paper.publish_date.strftime('%Y-%m-%d') if paper.publish_date else None,
                        'authors': paper.authors,
                        'attachment_path': paper.attachment_path,
                        'contract_path': paper.attachment_path,  # 兼容
                        'achievement_type': paper.achievement_type
                    }
                    for paper in papers
                ]
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取失败：{str(e)}'
            })
    
    elif request.method == 'POST':
        try:
            data = request.form.to_dict()
            # 字段兼容处理
            if 'achievement_name' in data:
                data['title'] = data.pop('achievement_name')
            if 'description' in data:
                data['journal'] = data.pop('description')
            file = request.files.get('attachment') or request.files.get('contract')
            if file:
                employee_number = current_user.employee_number
                date_prefix = datetime.now().strftime('%Y-%m-%d')
                filename = f"{date_prefix}_{file.filename}"
                upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'research_papers', str(employee_number))
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                data['attachment_path'] = f'research_papers/{employee_number}/{filename}'
            
            # 处理日期字段
            if 'publish_date' in data:
                data['publish_date'] = datetime.strptime(data['publish_date'], '%Y-%m-%d').date()
            
            data['teacher_id'] = current_user.id
            paper = ResearchPaper(**data)
            db.session.add(paper)
            db.session.commit()
            # 返回映射后的字段
            return jsonify({
                'success': True,
                'message': '添加成功',
                'data': {
                    'id': paper.id,
                    'achievement_type': paper.achievement_type,
                    'achievement_name': paper.title,
                    'description': paper.journal,
                    'contract_path': paper.attachment_path
                }
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'添加失败：{str(e)}'
            })

@app.route('/api/research_papers/<int:id>', methods=['DELETE'])
@login_required
def delete_research_paper(id):
    try:
        paper = ResearchPaper.query.get_or_404(id)
        if paper.teacher_id != current_user.id and not current_user.role == 'admin':
            return jsonify({'code': 403, 'message': '没有权限删除此论文'})
        # 删除附件
        if paper.attachment_path:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], paper.attachment_path))
            except:
                pass
        db.session.delete(paper)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 400, 'message': f'删除失败：{str(e)}'})

@app.route('/api/innovation_projects', methods=['GET'])
@login_required
def get_innovation_projects():
    try:
        projects = InnovationProject.query.filter_by(teacher_id=current_user.id).order_by(InnovationProject.start_date.desc()).all()
        return jsonify({
            'code': 200,
            'data': [
                {
                    'id': p.id,
                    'project_name': p.project_name,
                    'project_type': p.project_type,
                    'project_level': p.project_level,
                    'funding': p.funding,
                    'student_name': p.student_name,
                    'student_id': p.student_id,
                    'team_members': p.team_members,
                    'start_date': p.start_date.strftime('%Y-%m-%d') if p.start_date else '',
                    'end_date': p.end_date.strftime('%Y-%m-%d') if p.end_date else '',
                    'status': p.status,
                    'achievement': p.achievement,
                    'attachment_path': p.attachment_path,
                    'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S') if p.created_at else '',
                    'updated_at': p.updated_at.strftime('%Y-%m-%d %H:%M:%S') if p.updated_at else ''
                }
                for p in projects
            ]
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        })

@app.route('/api/competitions', methods=['GET', 'POST'])
@login_required
def handle_competitions():
    """处理学科竞赛的API"""
    if request.method == 'GET':
        # 获取当前用户的所有竞赛记录
        competitions = Competition.query.filter_by(teacher_id=current_user.id).all()
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': [competition.to_dict() for competition in competitions]
        })
    else:  # POST
        try:
            data = request.form.to_dict()
            
            # 处理日期字段
            if data.get('competition_date'):
                data['competition_date'] = datetime.strptime(data['competition_date'], '%Y-%m-%d')
            
            # 处理附件上传
            file = request.files.get('attachment')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = str(uuid.uuid4()) + '_' + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                data['attachment_path'] = unique_filename

            # 添加教师ID
            data['teacher_id'] = current_user.id
            
            # 创建新竞赛记录
            competition = Competition(**data)
            db.session.add(competition)
            db.session.commit()
            
            return jsonify({
                'code': 200,
                'message': '创建成功',
                'data': competition.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'code': 500,
                'message': f'创建失败：{str(e)}'
            })

@app.route('/api/innovation_projects/<int:id>', methods=['DELETE'])
@login_required
def delete_innovation_project(id):
    """删除创新创业项目"""
    try:
        project = InnovationProject.query.get_or_404(id)
        if project.teacher_id != current_user.id and not current_user.role == 'admin':
            return jsonify({'success': False, 'message': '没有权限删除此项目'})
        
        # 删除关联的附件
        if project.attachment_path:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], project.attachment_path))
            except:
                pass  # 如果文件不存在，继续执行
        
        db.session.delete(project)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败：{str(e)}'})

@app.route('/api/competitions/<int:id>', methods=['DELETE'])
@login_required
def delete_competition(id):
    """删除学科竞赛记录"""
    try:
        competition = Competition.query.get_or_404(id)
        if competition.teacher_id != current_user.id and not current_user.role == 'admin':
            return jsonify({'code': 403, 'message': '没有权限删除此记录'})
        
        # 删除关联的附件
        if competition.attachment_path:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], competition.attachment_path))
            except:
                pass  # 如果文件不存在，继续执行
        
        db.session.delete(competition)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'删除失败：{str(e)}'})

@app.route('/scientific_research')
@login_required
def scientific_research():
    """科研立项与成果页面"""
    return render_template('scientific_research.html')

@app.route('/college_events')
@login_required
def college_events():
    return render_template('college_events.html')

@app.route('/api/college_events', methods=['GET'])
@login_required
def get_college_events():
    try:
        events = CollegeEvent.query.order_by(CollegeEvent.event_date.desc()).all()
        return jsonify({'code': 200, 'data': [event.to_dict() for event in events]})
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)})

@app.route('/api/college_events', methods=['POST'])
@login_required
def add_college_event():
    # 检查用户权限（只有特定用户可以添加）
    if current_user.username not in ['张艳鹏', '王鹏']:
        return jsonify({'code': 403, 'message': '您没有权限执行此操作'})
    
    try:
        data = request.form
        attachment = request.files.get('attachment')
        attachment_path = None
        
        # 处理文件上传
        if attachment and attachment.filename:
            success, result, error_code = save_uploaded_file(attachment, app.config['UPLOAD_FOLDER'])
            if not success:
                if error_code == 1:  # 文件已存在
                    return jsonify({
                        'code': 409,  # HTTP 409 Conflict
                        'message': '文件已存在，请重命名后重试',
                        'error_code': error_code
                    })
                else:  # 其他错误
                    return jsonify({
                        'code': 400,
                        'message': result,
                        'error_code': error_code
                    })
            attachment_path = result
        
        event = CollegeEvent(
            title=data['title'],
            event_date=datetime.strptime(data['event_date'], '%Y-%m-%d').date(),
            description=data['description'],
            attachment_path=attachment_path,
            original_filename=attachment.filename if attachment else None,  # 添加原始文件名
            created_by=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({'code': 200, 'message': '添加成功'})
    except Exception as e:
        db.session.rollback()
        if attachment_path and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], attachment_path)):
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], attachment_path))
            except:
                pass
        return jsonify({'code': 500, 'message': str(e)})

@app.route('/api/college_events/<int:id>', methods=['DELETE'])
@login_required
def delete_college_event(id):
    # 检查用户权限（只有特定用户可以删除）
    if current_user.username not in ['张艳鹏', '王鹏']:
        return jsonify({'code': 403, 'message': '您没有权限执行此操作'})
    
    try:
        event = CollegeEvent.query.get_or_404(id)
        
        # 删除附件
        if event.attachment_path:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], event.attachment_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)})

@app.route('/api/innovation_projects', methods=['POST'])
@login_required
def add_innovation_project():
    try:
        data = request.form.to_dict()
        # 处理日期字段
        if data.get('start_date'):
            data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d')
        if data.get('end_date'):
            data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d')
        # 处理附件上传
        file = request.files.get('attachment')
        if file and allowed_file(file.filename):
            from datetime import datetime
            employee_number = current_user.employee_number or current_user.id
            date_prefix = datetime.now().strftime('%Y-%m-%d')
            filename = f"{date_prefix}_{file.filename}"
            upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'innovation_projects', str(employee_number))
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            data['attachment_path'] = f'innovation_projects/{employee_number}/{filename}'
        # 添加教师ID
        data['teacher_id'] = current_user.id
        # 创建新项目
        project = InnovationProject(**data)
        db.session.add(project)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '创建成功',
            'data': project.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'创建失败：{str(e)}'
        })

@app.route('/innovation_achievements')
@login_required
def innovation_achievements():
    """双创成果页面"""
    return render_template('innovation_achievements.html')

@app.route('/five_one_mentor')
@login_required
def five_one_mentor():
    """五业导师页面"""
    return render_template('five_one_mentor.html')

@app.route('/api/five_one_mentor/records', methods=['GET'])
@login_required
def get_mentor_records():
    """获取五业导师指导记录"""
    try:
        # 张艳鹏和王鹏可以看到所有记录
        if current_user.username in ['张艳鹏', '王鹏']:
            records = FiveOneMentor.query.join(
                User, FiveOneMentor.teacher_id == User.id
            ).add_columns(
                User.name.label('teacher_name')
            ).all()
            return jsonify([{
                'id': record.FiveOneMentor.id,
                'teacher_id': record.FiveOneMentor.teacher_id,
                'teacher_name': record.teacher_name,
                'student_name': record.FiveOneMentor.student_name,
                'student_id': record.FiveOneMentor.student_id,
                'class_name': record.FiveOneMentor.class_name,
                'photo_path': record.FiveOneMentor.photo_path,
                'status': record.FiveOneMentor.status,
                'review_comment': record.FiveOneMentor.review_comment,
                'created_at': record.FiveOneMentor.created_at.strftime('%Y-%m-%d %H:%M:%S') if record.FiveOneMentor.created_at else None
            } for record in records])
        else:
            # 普通教师只能看到自己的记录
            records = FiveOneMentor.query.filter_by(teacher_id=current_user.id).all()
            return jsonify([record.to_dict() for record in records])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/five_one_mentor/records', methods=['POST'])
@login_required
def add_mentor_record():
    """添加五业导师指导记录"""
    try:
        student_name = request.form.get('student_name')
        student_id = request.form.get('student_id')
        class_name = request.form.get('class_name')
        
        if not all([student_name, student_id, class_name]):
            return jsonify({'error': '请填写完整的学生信息'}), 400
            
        # 处理照片上传
        photo = request.files.get('photo')
        photo_path = None
        if photo and allowed_file(photo.filename):
            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.filename}")
            photo_path = os.path.join('student_photos', filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            photo.save(full_path)
            
        record = FiveOneMentor(
            teacher_id=current_user.id,
            student_name=student_name,
            student_id=student_id,
            class_name=class_name,
            photo_path=photo_path,
            status='pending',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/five_one_mentor/records/<int:id>', methods=['DELETE'])
@login_required
def delete_mentor_record(id):
    """删除五业导师指导记录"""
    try:
        record = FiveOneMentor.query.get_or_404(id)
        # 修改权限判断逻辑，使用用户名判断
        if record.teacher_id != current_user.id and current_user.username not in ['张艳鹏', '王鹏']:
            return jsonify({'error': '无权删除此记录'}), 403
            
        # 删除照片文件
        if record.photo_path:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], record.photo_path)
            if os.path.exists(photo_path):
                os.remove(photo_path)
                
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': '记录已删除'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/five_one_mentor/records/review', methods=['POST'])
@login_required
def review_mentor_records():
    """批量审核五业导师指导记录"""
    if current_user.username not in ['张艳鹏', '王鹏']:
        return jsonify({'error': '无权进行审核'}), 403
        
    try:
        data = request.get_json()
        record_ids = data.get('record_ids', [])
        status = data.get('status')
        comment = data.get('comment', '')
        
        if not record_ids or status not in ['approved', 'rejected']:
            return jsonify({'error': '参数错误'}), 400
            
        records = FiveOneMentor.query.filter(FiveOneMentor.id.in_(record_ids)).all()
        for record in records:
            record.status = status
            record.review_comment = comment
            record.reviewer_id = current_user.id
            record.review_date = datetime.now()
            record.updated_at = datetime.now()
            
        db.session.commit()
        return jsonify({'message': '审核完成'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/teacher/statistics', methods=['GET'])
def get_teacher_statistics():
    try:
        print("开始获取教师统计数据...")
        teachers = User.query.filter_by(role='teacher').all()
        print(f"找到 {len(teachers)} 名教师")

        # 初始化统计数据
        statistics = {
            'total': len(teachers),
            'age_structure': {'labels': [], 'values': []},
            'education_structure': {'labels': [], 'values': []},
            'title_structure': {'labels': [], 'values': []},
            'dual_teacher_structure': {'labels': ['是', '否'], 'values': [0, 0]},
            'gender_structure': {'labels': ['男', '女'], 'values': [0, 0]}
        }

        # 年龄结构统计
        age_ranges = {
            '30岁以下': 0,
            '31-40岁': 0,
            '41-50岁': 0,
            '51岁以上': 0
        }
        
        for teacher in teachers:
            if teacher.birth_date:
                age = (datetime.now().year - teacher.birth_date.year)
                if age <= 30:
                    age_ranges['30岁以下'] += 1
                elif age <= 40:
                    age_ranges['31-40岁'] += 1
                elif age <= 50:
                    age_ranges['41-50岁'] += 1
                else:
                    age_ranges['51岁以上'] += 1
        
        statistics['age_structure']['labels'] = list(age_ranges.keys())
        statistics['age_structure']['values'] = list(age_ranges.values())

        # 学历结构统计
        education_stats = {}
        for teacher in teachers:
            if teacher.education_level:
                education_stats[teacher.education_level] = education_stats.get(teacher.education_level, 0) + 1
        
        statistics['education_structure']['labels'] = list(education_stats.keys())
        statistics['education_structure']['values'] = list(education_stats.values())

        # 职称结构统计
        title_stats = {}
        for teacher in teachers:
            title = teacher.highest_title if teacher.highest_title else '未定职'
            title_stats[title] = title_stats.get(title, 0) + 1
        
        statistics['title_structure']['labels'] = list(title_stats.keys())
        statistics['title_structure']['values'] = list(title_stats.values())

        # 双师结构统计
        dual_teacher_count = {'是': 0, '否': 0}
        for teacher in teachers:
            if teacher.is_dual_teacher:
                dual_teacher_count['是'] += 1
            else:
                dual_teacher_count['否'] += 1
        
        statistics['dual_teacher_structure']['values'] = [dual_teacher_count['是'], dual_teacher_count['否']]

        # 性别结构统计
        gender_count = {'男': 0, '女': 0}
        for teacher in teachers:
            if teacher.gender in ['男', '女']:
                gender_count[teacher.gender] += 1
        
        statistics['gender_structure']['values'] = [gender_count['男'], gender_count['女']]

        print("统计数据处理完成")
        print(f"统计结果: {statistics}")
        
        return jsonify({
            'success': True,
            'data': statistics
        })
    except Exception as e:
        print(f"处理教师统计时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/user/info')
@login_required
def get_user_info():
    """获取当前用户信息的API端点"""
    try:
        user_info = current_user.to_dict()
        return jsonify({
            'code': 200,
            'data': user_info
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        })

@app.route('/api/courses', methods=['GET', 'POST'])
@login_required
def handle_courses():
    if request.method == 'GET':
        try:
            # 获取查询参数
            teacher_id = request.args.get('teacher_id')
            semester = request.args.get('semester')
            
            # 构建查询
            query = Course.query
            if teacher_id:
                query = query.filter(Course.teacher_id == teacher_id)
            if semester:
                query = query.filter(Course.semester == semester)
                
            courses = query.all()
            return jsonify({
                'success': True,
                'message': '获取成功',
                'data': [course.to_dict() for course in courses]
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取失败：{str(e)}'
            })
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            course = Course(**data)
            db.session.add(course)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': '创建成功',
                'data': course.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'创建失败：{str(e)}'
            })

@app.route('/api/courses/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def handle_course(id):
    course = Course.query.get_or_404(id)
    
    if request.method == 'PUT':
        try:
            data = request.get_json()
            for key, value in data.items():
                setattr(course, key, value)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': '更新成功',
                'data': course.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'更新失败：{str(e)}'
            })
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(course)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': '删除成功'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'删除失败：{str(e)}'
            })

@app.route('/api/scientific_projects', methods=['GET'])
@login_required
def get_scientific_projects():
    """获取科研立项列表"""
    try:
        if current_user.role == 'admin':
            projects = ScientificProject.query.all()
        else:
            projects = ScientificProject.query.filter_by(teacher_id=current_user.id).all()
        return jsonify({
            'success': True,
            'message': '获取科研立项列表成功',
            'data': [project.to_dict() for project in projects]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取科研立项列表失败：{str(e)}'
        })

@app.route('/api/scientific_projects', methods=['POST'])
@login_required
def add_scientific_project():
    """添加科研立项"""
    try:
        # 获取基本信息
        project_name = request.form.get('project_name')
        if not project_name:
            return jsonify({
                'success': False,
                'message': '项目名称不能为空'
            })

        # 创建新的科研立项记录
        project = ScientificProject(
            teacher_id=current_user.id,
            project_name=project_name
        )

        # 处理文件上传
        def save_file(file_obj, subfolder):
            if file_obj and file_obj.filename:
                from datetime import datetime
                employee_number = current_user.employee_number
                date_prefix = datetime.now().strftime('%Y-%m-%d')
                # 保留原始文件名（含中文），只加日期前缀
                filename = f"{date_prefix}_{file_obj.filename}"
                file_path = os.path.join('scientific_projects', str(employee_number), subfolder, filename)
                abs_path = os.path.join(app.config['UPLOAD_FOLDER'], file_path)
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                file_obj.save(abs_path)
                return file_path
            return None

        # 获取并保存文件
        approval_doc = request.files.get('approval_doc')
        notice_doc = request.files.get('notice_doc')
        completion_cert = request.files.get('completion_cert')

        project.approval_doc = save_file(approval_doc, 'approval')
        project.notice_doc = save_file(notice_doc, 'notice')
        project.completion_cert = save_file(completion_cert, 'completion')
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '添加科研立项成功',
            'data': project.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'添加科研立项失败：{str(e)}'
        })

@app.route('/api/scientific_projects/<int:project_id>', methods=['PUT'])
@login_required
def update_scientific_project(project_id):
    """更新科研立项"""
    try:
        project = ScientificProject.query.get(project_id)
        if not project:
            return jsonify({
                'success': False,
                'message': '科研立项不存在'
            })
            
        if current_user.role != 'admin' and project.teacher_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '无权限修改此科研立项'
            })
            
        data = request.get_json()
        
        # 更新字段
        for field in ['project_name', 'project_type', 'project_level', 'funding', 'status',
                     'approval_doc', 'notice_doc', 'completion_cert']:
            if field in data:
                setattr(project, field, data[field])
                
        # 处理日期字段
        if 'approval_date' in data:
            project.approval_date = datetime.strptime(data['approval_date'], '%Y-%m-%d') if data['approval_date'] else None
        if 'completion_date' in data:
            project.completion_date = datetime.strptime(data['completion_date'], '%Y-%m-%d') if data['completion_date'] else None
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '更新科研立项成功',
            'data': project.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'更新科研立项失败：{str(e)}'
        })

@app.route('/api/scientific_projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_scientific_project(project_id):
    """删除科研立项"""
    try:
        project = ScientificProject.query.get(project_id)
        if not project:
            return jsonify({
                'success': False,
                'message': '科研立项不存在'
            })
            
        if current_user.role != 'admin' and project.teacher_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '无权限删除此科研立项'
            })
            
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除科研立项成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除科研立项失败：{str(e)}'
        })

@app.route('/api/teaching_projects/<int:id>', methods=['DELETE'])
@login_required
def delete_teaching_project(id):
    try:
        project = TeachingProject.query.get_or_404(id)
        if project.teacher_id != current_user.id and not current_user.role == 'admin':
            return jsonify({'success': False, 'message': '没有权限删除此项目'})
        # 删除附件
        if project.attachment_path:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], project.attachment_path))
            except:
                pass
        db.session.delete(project)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败：{str(e)}'})

@app.route('/api/evaluation_projects/<int:id>', methods=['DELETE'])
@login_required
def delete_evaluation_project(id):
    try:
        project = EvaluationProject.query.get_or_404(id)
        if project.teacher_id != current_user.id and not current_user.role == 'admin':
            return jsonify({'success': False, 'message': '没有权限删除此项目'})
        # 删除附件
        if project.attachment_path:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], project.attachment_path))
            except:
                pass
        db.session.delete(project)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败：{str(e)}'})

@app.route('/api/scientific_awards', methods=['GET'])
@login_required
def get_scientific_awards():
    """获取科研奖励列表"""
    try:
        if current_user.role == 'admin':
            awards = ScientificAward.query.all()
        else:
            awards = ScientificAward.query.filter_by(teacher_id=current_user.id).all()
        # 字段映射
        data = []
        for award in awards:
            d = award.to_dict()
            data.append({
                'id': d['id'],
                'award_name': d['award_name'],
                'level': d.get('award_level', ''),
                'members': d.get('description', ''),
                'award_date': d['award_date'],
                'issuing_authority': d.get('awarding_body', ''),
            })
        return jsonify({
            'success': True,
            'message': '获取科研奖励列表成功',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取科研奖励列表失败：{str(e)}'
        })

@app.route('/api/scientific_awards', methods=['POST'])
@login_required
def add_scientific_award():
    """添加科研奖励"""
    try:
        award_name = request.form.get('award_name')
        if not award_name:
            return jsonify({'success': False, 'message': '奖项名称不能为空'})
        award_level = request.form.get('level') or request.form.get('award_level')
        # 优先用members字段
        description = request.form.get('members') or request.form.get('description')
        award_date = request.form.get('award_date')
        awarding_body = request.form.get('issuing_authority') or request.form.get('awarding_body')
        # 处理文件上传（如有）
        attachment = request.files.get('attachment')
        def save_file(file_obj):
            if file_obj and file_obj.filename:
                from datetime import datetime
                employee_number = current_user.employee_number or current_user.id
                date_prefix = datetime.now().strftime('%Y-%m-%d')
                filename = f"{date_prefix}_{file_obj.filename}"
                file_path = os.path.join('scientific_awards', str(employee_number), filename)
                abs_path = os.path.join(app.config['UPLOAD_FOLDER'], file_path)
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                file_obj.save(abs_path)
                return file_path
            return None
        attachment_path = save_file(attachment)
        award = ScientificAward(
            teacher_id=current_user.id,
            award_name=award_name,
            award_level=award_level,
            award_date=datetime.strptime(award_date, '%Y-%m-%d') if award_date else None,
            awarding_body=awarding_body,
            description=description,
            attachment_path=attachment_path
        )
        db.session.add(award)
        db.session.commit()
        return jsonify({'success': True, 'message': '添加科研奖励成功', 'data': award.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'添加科研奖励失败：{str(e)}'})

@app.route('/api/scientific_awards/<int:award_id>', methods=['DELETE'])
@login_required
def delete_scientific_award(award_id):
    """删除科研奖励"""
    try:
        award = ScientificAward.query.get(award_id)
        if not award:
            return jsonify({'success': False, 'message': '科研奖励不存在'})
        if current_user.role != 'admin' and award.teacher_id != current_user.id:
            return jsonify({'success': False, 'message': '无权限删除此科研奖励'})
        db.session.delete(award)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除科研奖励成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除科研奖励失败：{str(e)}'})

@app.route('/faculty_team')
@login_required
def faculty_team():
    """师资队伍页面"""
    # 检查权限
    if current_user.username not in ['张艳鹏', '王鹏', '高日月']:
        flash('您没有权限访问该页面')
        return redirect(url_for('profile'))
    
    # 获取所有教师信息
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('faculty_team.html', teachers=teachers)

@app.route('/faculty_team/view/<int:id>')
@login_required
def view_faculty_member(id):
    """查看教师详情"""
    # 检查权限
    if current_user.username not in ['张艳鹏', '王鹏', '高日月']:
        flash('您没有权限访问该页面')
        return redirect(url_for('profile'))
    
    teacher = User.query.get_or_404(id)
    return render_template('teacher_detail.html', teacher=teacher)

if __name__ == '__main__':
    # 自动执行数据库备份（纯Python实现，跨平台）
    db_file = os.path.join(os.path.dirname(__file__), 'university.db')
    backup_dir = os.path.join(os.path.dirname(__file__), '../db_backup')
    backup_file = os.path.join(backup_dir, 'university_backup.db')
    os.makedirs(backup_dir, exist_ok=True)
    try:
        if os.path.exists(backup_file):
            os.remove(backup_file)
        shutil.copy2(db_file, backup_file)
        print(f"数据库备份完成，备份文件：{backup_file}")
    except Exception as e:
        print(f"自动备份失败：{e}")

    # 自动备份 uploads 文件夹
    uploads_dir = os.path.join(os.path.dirname(__file__), '../uploads')
    uploads_backup_dir = os.path.join(os.path.dirname(__file__), '../uploads_backup')
    try:
        if os.path.exists(uploads_backup_dir):
            shutil.rmtree(uploads_backup_dir)
        if os.path.exists(uploads_dir):
            shutil.copytree(uploads_dir, uploads_backup_dir)
            print(f"附件备份完成，备份文件夹：{uploads_backup_dir}")
        else:
            print("未找到 uploads 文件夹，无需备份附件。")
    except Exception as e:
        print(f"附件自动备份失败：{e}")

    with app.app_context():
        db.create_all()  # 创建所有表
    app.run(debug=True)
