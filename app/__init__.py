from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from datetime import datetime

# Глобальные объекты расширений
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)

    # Регистрация blueprint (маршрутов)
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Импорт моделей для создания таблиц
    from app import models

    # Загрузчик пользователя для Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))
    
    # Регистрация фильтра для форматирования даты
    @app.template_filter('datetimeformat')
    def datetimeformat(timestamp):
        """Конвертирует timestamp в читаемую дату"""
        if timestamp:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime('%d.%m.%Y %H:%M:%S')
        return '—'

    return app