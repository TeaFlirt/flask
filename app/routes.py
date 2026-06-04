from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import User, Teacher, Student
from app.forms import RegistrationForm, LoginForm, TeacherForm, StudentForm

bp = Blueprint('main', __name__)

# ---------- Разрешенные расширения для фото ----------
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_photo(file, folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Добавляем уникальный префикс
        from datetime import datetime
        unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file_path = os.path.join(folder, unique_name)
        file.save(file_path)
        return f'/images/{folder.split("/")[-1]}/{unique_name}'
    return None

# ---------- Обычные страницы ----------
@bp.route('/')
def index():
    photos = ['images/pages/main1.jpg', 'images/pages/main2.jpg', 'images/pages/main3.jpg']
    return render_template('index.html', photos=photos)

@bp.route('/about')
def about():
    photos = ['images/pages/about1.jpg', 'images/pages/about2.jpg', 'images/pages/about3.jpg', 'images/pages/about4.jpg', 'images/pages/about5.jpg']
    return render_template('about.html', photos=photos)

@bp.route('/contacts')
def contacts():
    photos = ['images/pages/contacts1.jpg', 'images/pages/contacts2.jpg', 'images/pages/contacts3.jpg', 'images/pages/contacts4.jpg', 'images/pages/contacts5.jpg', 'images/pages/contacts6.jpg']
    return render_template('contacts.html', photos=photos)

# ---------- Страницы преподавателей ----------
@bp.route('/teachers')
def teachers():
    teachers_list = Teacher.query.filter_by(is_active=True).all()
    return render_template('teachers.html', teachers=teachers_list)

@bp.route('/teachers/<int:id>')
def show_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    return render_template('show_teacher.html', teacher=teacher)

@bp.route('/teachers/create', methods=['GET', 'POST'])
@login_required
def create_teacher():
    if not current_user.is_admin:
        abort(403)
    form = TeacherForm()
    if form.validate_on_submit():
        photo_path = None
        if form.photo.data:
            photo_path = save_photo(form.photo.data, 'app/static/images/teachers')
        
        teacher = Teacher(
            full_name=form.full_name.data,
            specialization=form.specialization.data,
            email=form.email.data,
            phone=form.phone.data,
            experience_years=form.experience_years.data,
            salary=form.salary.data,
            photo_path=photo_path or '/images/teachers/default.jpg',
            is_active=bool(form.is_active.data)
        )
        db.session.add(teacher)
        db.session.commit()
        flash('Преподаватель добавлен!', 'success')
        return redirect(url_for('main.teachers'))
    return render_template('create_teacher.html', form=form)

@bp.route('/teachers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    if not current_user.is_admin:
        abort(403)
    teacher = Teacher.query.get_or_404(id)
    form = TeacherForm(obj=teacher)
    if form.validate_on_submit():
        teacher.full_name = form.full_name.data
        teacher.specialization = form.specialization.data
        teacher.email = form.email.data
        teacher.phone = form.phone.data
        teacher.experience_years = form.experience_years.data
        teacher.salary = form.salary.data
        teacher.is_active = bool(form.is_active.data)
        
        if form.photo.data:
            photo_path = save_photo(form.photo.data, 'app/static/images/teachers')
            if photo_path:
                teacher.photo_path = photo_path
        
        db.session.commit()
        flash('Преподаватель обновлён!', 'success')
        return redirect(url_for('main.show_teacher', id=teacher.id))
    return render_template('edit_teacher.html', form=form, teacher=teacher)

@bp.route('/teachers/<int:id>/delete', methods=['POST'])
@login_required
def delete_teacher(id):
    if not current_user.is_admin:
        abort(403)
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Преподаватель удалён.', 'info')
    return redirect(url_for('main.teachers'))

# ---------- Страницы студентов ----------
@bp.route('/students')
def students():
    students_list = Student.query.filter_by(is_active=True).all()
    return render_template('students.html', students=students_list)

@bp.route('/students/<int:id>')
def show_student(id):
    student = Student.query.get_or_404(id)
    return render_template('show_student.html', student=student)

@bp.route('/students/create', methods=['GET', 'POST'])
@login_required
def create_student():
    if not current_user.is_admin:
        abort(403)
    form = StudentForm()
    if form.validate_on_submit():
        photo_path = None
        if form.photo.data:
            photo_path = save_photo(form.photo.data, 'app/static/images/students')
        
        student = Student(
            full_name=form.full_name.data,
            birth_date=form.birth_date.data,
            group=form.group.data,
            course=form.course.data,
            specialty=form.specialty.data,
            phone=form.phone.data,
            photo_path=photo_path or '/images/students/default.jpg',
            is_active=bool(form.is_active.data)
        )
        db.session.add(student)
        db.session.commit()
        flash('Студент добавлен!', 'success')
        return redirect(url_for('main.students'))
    return render_template('create_student.html', form=form)

@bp.route('/students/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    if not current_user.is_admin:
        abort(403)
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.full_name = form.full_name.data
        student.birth_date = form.birth_date.data
        student.group = form.group.data
        student.course = form.course.data
        student.specialty = form.specialty.data
        student.phone = form.phone.data
        student.is_active = bool(form.is_active.data)
        
        if form.photo.data:
            photo_path = save_photo(form.photo.data, 'app/static/images/students')
            if photo_path:
                student.photo_path = photo_path
        
        db.session.commit()
        flash('Студент обновлён!', 'success')
        return redirect(url_for('main.show_student', id=student.id))
    return render_template('edit_student.html', form=form, student=student)

@bp.route('/students/<int:id>/delete', methods=['POST'])
@login_required
def delete_student(id):
    if not current_user.is_admin:
        abort(403)
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Студент удалён.', 'info')
    return redirect(url_for('main.students'))

# ---------- Аутентификация ----------
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, is_admin=False)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Добро пожаловать, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        flash('Неверный email или пароль.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли.', 'info')
    return redirect(url_for('main.index'))

# ---------- Ошибка 404 ----------
@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404