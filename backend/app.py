from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from sqlalchemy import func
from functools import wraps

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'university.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 数据模型
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, user
    name = db.Column(db.String(80))
    major = db.Column(db.String(100))
    teaching_group = db.Column(db.String(100))
    is_dual_teacher = db.Column(db.String(10))
    award_title = db.Column(db.String(200))
    talent_title = db.Column(db.String(200))
    gender = db.Column(db.String(10))
    ethnicity = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    id_number = db.Column(db.String(18))
    political_status = db.Column(db.String(50))
    party_join_date = db.Column(db.Date)
    party_branch = db.Column(db.String(100))
    hometown = db.Column(db.String(100))
    position = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    education_level = db.Column(db.String(50))
    degree = db.Column(db.String(50))
    education_date = db.Column(db.Date)
    degree_date = db.Column(db.Date)
    bachelor_school = db.Column(db.String(100))
    master_school = db.Column(db.String(100))
    phd_school = db.Column(db.String(100))
    research_direction = db.Column(db.String(200))
    work_start_date = db.Column(db.Date)
    career_start_date = db.Column(db.Date)
    highest_title = db.Column(db.String(50))
    highest_title_date = db.Column(db.Date)
    files = db.relationship('File', backref='owner', lazy=True)
    employee_number = db.Column(db.Integer, default=0)  # 工号
    department = db.Column(db.String(100))
    photo_path = db.Column(db.String(200))
    subject = db.Column(db.String(50))
    teaching_team = db.Column(db.String(100))
    research_team = db.Column(db.String(100))
    project_group = db.Column(db.String(100))

    @property
    def age(self):
        """计算年龄"""
        if not self.birth_date:
            return None
        today = datetime.now()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('用户名或密码错误')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        try:
            # 处理基本信息
            current_user.name = request.form.get('name')
            current_user.gender = request.form.get('gender')
            current_user.ethnicity = request.form.get('ethnicity')
            current_user.political_status = request.form.get('political_status')
            current_user.party_branch = request.form.get('party_branch')
            current_user.education_level = request.form.get('education_level')  # 添加学历字段处理
            current_user.degree = request.form.get('degree')  # 添加学位字段处理
            
            # 处理日期字段
            birth_date = request.form.get('birth_date')
            if birth_date:
                current_user.birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
            
            party_join_date = request.form.get('party_join_date')
            if party_join_date:
                current_user.party_join_date = datetime.strptime(party_join_date, '%Y-%m-%d')
            
            education_date = request.form.get('education_date')  # 添加学历获得时间处理
            if education_date:
                current_user.education_date = datetime.strptime(education_date, '%Y-%m-%d')
                
            degree_date = request.form.get('degree_date')  # 添加学位获得时间处理
            if degree_date:
                current_user.degree_date = datetime.strptime(degree_date, '%Y-%m-%d')
            
            # ... 其他字段处理 ...

            # 如果提供了新密码
            password = request.form.get('password')
            if password:
                if password != request.form.get('confirm_password'):
                    return render_template('profile.html', error='两次输入的密码不一致')
                current_user.password_hash = generate_password_hash(password)

            db.session.commit()
            flash('个人信息更新成功！')
            return render_template('profile.html')
        except Exception as e:
            db.session.rollback()
            return render_template('profile.html', error=str(e))

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

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/teachers')
@login_required
def list_teachers():
    if current_user.role == 'admin':
        # 管理员可以看到所有教师
        teachers = User.query.filter_by(role='teacher').all()
    else:
        # 普通教师只能看到自己
        teachers = [current_user]
    return render_template('teachers.html', teachers=teachers)

@app.route('/teacher/<int:id>')
@login_required
def view_teacher(id):
    teacher = User.query.get_or_404(id)
    if current_user.role != 'admin' and current_user.id != id:
        flash('您没有权限查看此教师信息')
        return redirect(url_for('index'))
    return render_template('teacher_detail.html', teacher=teacher)

# 定义有效的职称列表
VALID_TITLES = ['教授', '副教授', '讲师', '助教']

@app.route('/teacher/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
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
    if current_user.role != 'admin':
        flash('只有管理员可以访问此页面')
        return redirect(url_for('dashboard'))
    
    # 获取教师总数
    total_teachers = User.query.filter_by(role='teacher').count()
    
    # 按职称统计
    title_stats = db.session.query(
        User.title, func.count(User.id)
    ).filter(
        User.role == 'teacher'
    ).group_by(User.title).all()
    
    # 按性别统计
    gender_stats = db.session.query(
        User.gender, func.count(User.id)
    ).filter(
        User.role == 'teacher'
    ).group_by(User.gender).all()
    
    # 按年龄段统计
    current_year = datetime.now().year
    age_ranges = {
        '35岁以下': 0,
        '36-45岁': 0,
        '46-55岁': 0,
        '56岁以上': 0
    }
    
    teachers = User.query.filter_by(role='teacher').all()
    for teacher in teachers:
        if teacher.birth_date:
            age = current_year - teacher.birth_date.year
            if age <= 35:
                age_ranges['35岁以下'] += 1
            elif age <= 45:
                age_ranges['36-45岁'] += 1
            elif age <= 55:
                age_ranges['46-55岁'] += 1
            else:
                age_ranges['56岁以上'] += 1
    
    # 按工作年限统计
    work_years_ranges = {
        '5年以下': 0,
        '5-10年': 0,
        '11-20年': 0,
        '20年以上': 0
    }
    
    for teacher in teachers:
        if teacher.work_start_date:
            years = current_year - teacher.work_start_date.year
            if years <= 5:
                work_years_ranges['5年以下'] += 1
            elif years <= 10:
                work_years_ranges['5-10年'] += 1
            elif years <= 20:
                work_years_ranges['11-20年'] += 1
            else:
                work_years_ranges['20年以上'] += 1
    
    return render_template('teacher_statistics.html',
                         total_teachers=total_teachers,
                         title_stats=title_stats,
                         gender_stats=gender_stats,
                         age_ranges=age_ranges,
                         work_years_ranges=work_years_ranges)

@app.route('/api/teachers/<int:id>', methods=['PUT'])
@login_required
def update_teacher(id):
    if current_user.role != 'admin':
        return jsonify({'error': '没有权限进行此操作'}), 403
    
    teacher = User.query.get_or_404(id)
    data = request.get_json()
    
    if 'employee_number' in data:
        teacher.employee_number = data['employee_number']
        
    try:
        db.session.commit()
        return jsonify({'message': '更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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
        return redirect(url_for('list_teachers'))
    
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
    
    return redirect(url_for('list_teachers'))

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
        current_user.password_hash = generate_password_hash(password)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)