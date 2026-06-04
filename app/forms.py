from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, DecimalField, FileField
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
    salary = DecimalField('Зарплата', places=2, default=0.00)
    photo = FileField('Фото преподавателя', validators=[DataRequired()])
    is_active = SelectField('Статус', choices=[(1, 'Активен'), (0, 'Неактивен')], coerce=int, default=1)
    submit = SubmitField('Сохранить')

class StudentForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(max=255)])
    birth_date = StringField('Дата рождения (ДД.ММ.ГГГГ)', validators=[DataRequired(), Length(max=10)])
    group = StringField('Группа', validators=[DataRequired(), Length(max=50)])
    course = IntegerField('Курс', validators=[NumberRange(1, 5)], default=1)
    specialty = StringField('Специальность', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Телефон', validators=[Optional(), Length(max=20)])
    photo = FileField('Фото студента', validators=[DataRequired()])
    is_active = SelectField('Статус', choices=[(1, 'Активен'), (0, 'Неактивен')], coerce=int, default=1)
    submit = SubmitField('Сохранить')