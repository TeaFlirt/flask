from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Teacher, Gallery
from app.forms import RegistrationForm, LoginForm, TeacherForm, GalleryForm
import math
from app.models import CalculatorHistory
from app.forms import CalculatorForm

bp = Blueprint('main', __name__)

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

# ---------- Таблицы ----------
@bp.route('/gallery')
def gallery():
    images = Gallery.query.filter_by(is_published=1).order_by(Gallery.sort_order).all()
    return render_template('gallery.html', images=images)

@bp.route('/teachers')
def teachers():
    teachers_list = Teacher.query.filter_by(status=1).all()
    return render_template('teachers.html', teachers=teachers_list)

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

# ---------- CRUD Teachers ----------
def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)

@bp.route('/teachers/<int:id>')
def show_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    return render_template('show_teacher.html', teacher=teacher)

@bp.route('/teachers/create', methods=['GET', 'POST'])
@login_required
def create_teacher():
    admin_required()
    form = TeacherForm()
    if form.validate_on_submit():
        teacher = Teacher(
            full_name=form.full_name.data,
            specialization=form.specialization.data,
            email=form.email.data,
            phone=form.phone.data,
            experience_years=form.experience_years.data,
            education=form.education.data,
            photo_path=form.photo_path.data,
            salary=form.salary.data,
            status=form.status.data
        )
        db.session.add(teacher)
        db.session.commit()
        flash('Преподаватель добавлен!', 'success')
        return redirect(url_for('main.teachers'))
    return render_template('create_teacher.html', form=form)

@bp.route('/teachers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    admin_required()
    teacher = Teacher.query.get_or_404(id)
    form = TeacherForm(obj=teacher)
    if form.validate_on_submit():
        teacher.full_name = form.full_name.data
        teacher.specialization = form.specialization.data
        teacher.email = form.email.data
        teacher.phone = form.phone.data
        teacher.experience_years = form.experience_years.data
        teacher.education = form.education.data
        teacher.photo_path = form.photo_path.data
        teacher.salary = form.salary.data
        teacher.status = form.status.data
        db.session.commit()
        flash('Преподаватель обновлён!', 'success')
        return redirect(url_for('main.show_teacher', id=teacher.id))
    return render_template('edit_teacher.html', form=form, teacher=teacher)

@bp.route('/teachers/<int:id>/delete', methods=['POST'])
@login_required
def delete_teacher(id):
    admin_required()
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Преподаватель удалён.', 'info')
    return redirect(url_for('main.teachers'))

# ---------- CRUD Gallery ----------
@bp.route('/gallery/<int:id>')
def show_gallery(id):
    image = Gallery.query.get_or_404(id)
    return render_template('show_gallery.html', image=image)

@bp.route('/gallery/create', methods=['GET', 'POST'])
@login_required
def create_gallery():
    admin_required()
    form = GalleryForm()
    if form.validate_on_submit():
        gallery = Gallery(
            title=form.title.data,
            description=form.description.data,
            file_path=form.file_path.data,
            file_size=form.file_size.data,
            mime_type=form.mime_type.data,
            width=form.width.data,
            height=form.height.data,
            category=form.category.data,
            sort_order=form.sort_order.data,
            is_published=form.is_published.data
        )
        db.session.add(gallery)
        db.session.commit()
        flash('Фотография добавлена!', 'success')
        return redirect(url_for('main.gallery'))
    return render_template('create_gallery.html', form=form)

@bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_gallery(id):
    admin_required()
    image = Gallery.query.get_or_404(id)
    form = GalleryForm(obj=image)
    if form.validate_on_submit():
        image.title = form.title.data
        image.description = form.description.data
        image.file_path = form.file_path.data
        image.file_size = form.file_size.data
        image.mime_type = form.mime_type.data
        image.width = form.width.data
        image.height = form.height.data
        image.category = form.category.data
        image.sort_order = form.sort_order.data
        image.is_published = form.is_published.data
        db.session.commit()
        flash('Изображение обновлено!', 'success')
        return redirect(url_for('main.show_gallery', id=image.id))
    return render_template('edit_gallery.html', form=form, image=image)

@bp.route('/gallery/<int:id>/delete', methods=['POST'])
@login_required
def delete_gallery(id):
    admin_required()
    image = Gallery.query.get_or_404(id)
    db.session.delete(image)
    db.session.commit()
    flash('Изображение удалено.', 'info')
    return redirect(url_for('main.gallery'))

# ---------- Калькулятор ----------
@bp.route('/calculator', methods=['GET', 'POST'])
def calculator():
    form = CalculatorForm()
    result = None
    error = None
    
    if form.validate_on_submit():
        try:
            # Преобразуем первый операнд
            operand1 = float(form.operand1.data.replace(',', '.'))
            operation = form.operation.data
            
            # Для бинарных операций нужен второй операнд
            if operation in ['+', '-', '*', '/', '^']:
                if not form.operand2.data:
                    error = 'Введите второе число'
                else:
                    operand2 = float(form.operand2.data.replace(',', '.'))
                    
                    if operation == '+':
                        result = operand1 + operand2
                        expression = f"{operand1} + {operand2}"
                    elif operation == '-':
                        result = operand1 - operand2
                        expression = f"{operand1} - {operand2}"
                    elif operation == '*':
                        result = operand1 * operand2
                        expression = f"{operand1} × {operand2}"
                    elif operation == '/':
                        if operand2 == 0:
                            error = 'Деление на ноль невозможно!'
                        else:
                            result = operand1 / operand2
                            expression = f"{operand1} ÷ {operand2}"
                    elif operation == '^':
                        result = operand1 ** operand2
                        expression = f"{operand1} ^ {operand2}"
            
            # Унарная операция 1/x
            elif operation == '1/x':
                if operand1 == 0:
                    error = 'Деление на ноль невозможно!'
                else:
                    result = 1 / operand1
                    expression = f"1 / {operand1}"
                    operand2 = None  # нет второго операнда
            
            # Если нет ошибки, сохраняем в историю
            if not error and result is not None:
                # Форматируем результат (убираем .0 если число целое)
                if result == int(result):
                    result_str = str(int(result))
                else:
                    result_str = str(round(result, 10))
                
                # Получаем IP пользователя
                ip_address = request.remote_addr
                user_id = current_user.id if current_user.is_authenticated else None
                
                # Сохраняем в БД
                history = CalculatorHistory(
                    expression=expression,
                    result=result_str,
                    operation=operation,
                    operand1=operand1,
                    operand2=operand2,
                    ip_address=ip_address,
                    user_id=user_id
                )
                db.session.add(history)
                db.session.commit()
                
                flash(f'Результат: {expression} = {result_str}', 'success')
                
        except ValueError:
            error = 'Пожалуйста, введите корректные числа'
        except OverflowError:
            error = 'Результат слишком большой!'
        except Exception as e:
            error = f'Ошибка: {str(e)}'
    
    return render_template('calculator.html', form=form, result=result, error=error)

@bp.route('/calculator/history')
def calculator_history():
    # Получаем историю: админы видят все, обычные пользователи - свои, гости - по IP
    if current_user.is_authenticated and current_user.is_admin:
        history = CalculatorHistory.query.order_by(CalculatorHistory.created_at.desc()).limit(100).all()
    elif current_user.is_authenticated:
        history = CalculatorHistory.query.filter_by(user_id=current_user.id)\
            .order_by(CalculatorHistory.created_at.desc()).limit(50).all()
    else:
        ip_address = request.remote_addr
        history = CalculatorHistory.query.filter_by(ip_address=ip_address, user_id=None)\
            .order_by(CalculatorHistory.created_at.desc()).limit(50).all()
    
    return render_template('calculator_history.html', history=history)

@bp.route('/calculator/history/clear', methods=['POST'])
def clear_calculator_history():
    # Очистка истории с учетом прав
    if current_user.is_authenticated and current_user.is_admin:
        CalculatorHistory.query.delete()
        db.session.commit()
        flash('Вся история калькулятора очищена', 'info')
    elif current_user.is_authenticated:
        CalculatorHistory.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('Ваша история калькулятора очищена', 'info')
    else:
        ip_address = request.remote_addr
        CalculatorHistory.query.filter_by(ip_address=ip_address, user_id=None).delete()
        db.session.commit()
        flash('Ваша история калькулятора очищена', 'info')
    
    return redirect(url_for('main.calculator_history'))

@bp.route('/calculator/history/delete/<int:id>', methods=['POST'])
def delete_calculator_entry(id):
    entry = CalculatorHistory.query.get_or_404(id)
    
    # Проверка прав на удаление
    can_delete = False
    if current_user.is_authenticated and current_user.is_admin:
        can_delete = True
    elif current_user.is_authenticated and entry.user_id == current_user.id:
        can_delete = True
    elif not current_user.is_authenticated and entry.user_id is None and entry.ip_address == request.remote_addr:
        can_delete = True
    
    if can_delete:
        db.session.delete(entry)
        db.session.commit()
        flash('Запись удалена', 'success')
    else:
        abort(403)
    
    return redirect(url_for('main.calculator_history'))

# ---------- Ошибка 404 ----------
@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404