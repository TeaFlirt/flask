from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # имя таблицы в MySQL

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
    full_name = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    education = db.Column(db.Text, nullable=False)
    photo_path = db.Column(db.String(255), nullable=True)
    salary = db.Column(db.Numeric(10,2), default=0.00)
    status = db.Column(db.Integer, default=1)  # 1-активен
    created_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()))
    updated_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()), onupdate=lambda: int(datetime.now().timestamp()))

    def __repr__(self):
        return f'<Teacher {self.full_name}>'


class Gallery(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, default=0)
    mime_type = db.Column(db.String(100), default='image/jpeg')
    width = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), default='other')
    sort_order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Integer, default=1)   # 1-да, 0-нет
    uploaded_by = db.Column(db.Integer, nullable=True)  # id пользователя
    created_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()))
    updated_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()), onupdate=lambda: int(datetime.now().timestamp()))

    def __repr__(self):
        return f'<Gallery {self.title}>'


class CalculatorHistory(db.Model):
    __tablename__ = 'calculator_history'
    
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(500), nullable=False)  # исходное выражение
    result = db.Column(db.String(100), nullable=False)      # результат
    operation = db.Column(db.String(20), nullable=False)    # тип операции
    operand1 = db.Column(db.Float, nullable=False)          # первый операнд
    operand2 = db.Column(db.Float, nullable=True)           # второй операнд (для унарных операций - NULL)
    ip_address = db.Column(db.String(45), nullable=True)    # IP пользователя
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # если пользователь авторизован
    created_at = db.Column(db.Integer, default=lambda: int(datetime.now().timestamp()))
    
    # Связь с пользователем
    user = db.relationship('User', backref='calculations')
    
    def __repr__(self):
        return f'<CalculatorHistory {self.expression} = {self.result}>'