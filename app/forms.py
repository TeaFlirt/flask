from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, NumberRange
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято. Выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class TeacherForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(max=255)])
    specialization = StringField('Специализация', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    phone = StringField('Телефон', validators=[DataRequired(), Length(max=20)])
    experience_years = IntegerField('Стаж (лет)', validators=[NumberRange(0, 60)], default=0)
    education = TextAreaField('Образование', validators=[DataRequired()])
    photo_path = StringField('Путь к фото', validators=[Optional(), Length(max=255)])
    salary = DecimalField('Зарплата', places=2, default=0.00)
    status = SelectField('Статус', choices=[(1, 'Активен'), (0, 'Неактивен')], coerce=int, default=1)
    submit = SubmitField('Сохранить')

class GalleryForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Описание', validators=[Optional()])
    file_path = StringField('Путь к файлу', validators=[DataRequired(), Length(max=255)])
    file_size = IntegerField('Размер (байты)', default=0)
    mime_type = StringField('MIME-тип', default='image/jpeg')
    width = IntegerField('Ширина (px)', default=0)
    height = IntegerField('Высота (px)', default=0)
    category = StringField('Категория', default='other')
    sort_order = IntegerField('Порядок сортировки', default=0)
    is_published = SelectField('Опубликовано', choices=[(1, 'Да'), (0, 'Нет')], coerce=int, default=1)
    submit = SubmitField('Сохранить')

class CalculatorForm(FlaskForm):
    operand1 = StringField('Первое число', validators=[DataRequired()])
    operand2 = StringField('Второе число', validators=[Optional()])  # необязательно для унарных операций
    operation = SelectField('Операция', choices=[
        ('+', '+ (сложение)'),
        ('-', '- (вычитание)'),
        ('*', '* (умножение)'),
        ('/', '/ (деление)'),
        ('^', '^ (возведение в степень)'),
        ('1/x', '1/x (обратное число)')
    ], validators=[DataRequired()])
    submit = SubmitField('Вычислить')