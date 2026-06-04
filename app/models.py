from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()))
    updated_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()), onupdate=lambda: int(datetime.now().timestamp()))

    def __repr__(self):
        return f'<User {self.username}>'


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)           # Строка
    specialization = db.Column(db.String(100), nullable=False)      # Строка
    email = db.Column(db.String(255), nullable=False)               # Строка
    phone = db.Column(db.String(20), nullable=False)                # Строка
    experience_years = db.Column(db.Integer, default=0)             # Целое число
    salary = db.Column(db.Numeric(10,2), default=0.00)              # Дробное число
    photo_path = db.Column(db.String(255), nullable=False)          # Строка (ОБЯЗАТЕЛЬНО)
    is_active = db.Column(db.Boolean, default=True)                 # Булево значение
    created_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()))
    updated_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()), onupdate=lambda: int(datetime.now().timestamp()))

    def __repr__(self):
        return f'<Teacher {self.full_name}>'


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)           # Строка (ФИО)
    birth_date = db.Column(db.String(10), nullable=False)           # Строка (Дата рождения)
    group = db.Column(db.String(50), nullable=False)                # Строка (Группа)
    course = db.Column(db.Integer, default=1)                       # Целое число (Курс)
    specialty = db.Column(db.String(100), nullable=False)           # Строка (Специальность)
    phone = db.Column(db.String(20), nullable=True)                 # Строка (Телефон)
    photo_path = db.Column(db.String(255), nullable=False)          # Строка (ОБЯЗАТЕЛЬНО)
    is_active = db.Column(db.Boolean, default=True)                 # Булево значение
    created_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()))
    updated_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()), onupdate=lambda: int(datetime.now().timestamp()))

    def __repr__(self):
        return f'<Student {self.full_name}>'