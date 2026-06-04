#!/usr/bin/env python3
import time
import random
from app import create_app, db
from app.models import User, Teacher, Gallery
from werkzeug.security import generate_password_hash
from faker import Faker

fake = Faker('ru_RU')

SPECIALIZATIONS = [
    'Фортепиано', 'Скрипка', 'Виолончель', 'Гитара классическая', 'Гитара электрогитара',
    'Вокал академический', 'Вокал эстрадный', 'Флейта', 'Кларнет', 'Саксофон',
    'Труба', 'Ударные инструменты', 'Теория музыки', 'Сольфеджио', 'Дирижирование',
    'Арфа', 'Баян', 'Аккордеон', 'Контрабас', 'Синтезатор', 'Джазовая импровизация'
]

GALLERY_CATEGORIES = ['interior', 'classrooms', 'concerts', 'events', 'students', 'teachers']

# Базовые пути (только 5 вариантов)
TEACHER_PHOTO_BASE = '/images/teachers/teacher_'
GALLERY_IMAGE_BASE = '/images/gallery/gallery_'

def random_teacher_photo():
    num = random.randint(1, 5)
    return f"{TEACHER_PHOTO_BASE}{num}.jpg"

def random_gallery_photo():
    num = random.randint(1, 5)
    return f"{GALLERY_IMAGE_BASE}{num}.jpg"

def create_admin():
    admin_email = 'admin@harmony-school.ru'
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            username='admin',
            email=admin_email,
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            created_at=int(time.time()),
            updated_at=int(time.time())
        )
        db.session.add(admin)
        print('✅ Администратор создан: admin@harmony-school.ru / admin123')
    else:
        print('ℹ️ Администратор уже существует')

def create_teachers(count=100):
    existing = Teacher.query.count()
    if existing >= count:
        print(f'ℹ️ В базе уже {existing} преподавателей, генерация пропущена.')
        return

    teachers = []
    for i in range(count):
        full_name = fake.name_male() if i % 2 == 0 else fake.name_female()
        if random.choice([True, False]) and ' ' in full_name:
            parts = full_name.split()
            if len(parts) >= 2:
                full_name = f"{parts[0]} {fake.middle_name()} {parts[1]}"

        # Образование
        try:
            education = f"{fake.university_name()} — {fake.job()}"
        except AttributeError:
            education = random.choice([
                "Московская консерватория — преподаватель фортепиано",
                "РАМ им. Гнесиных — вокальное искусство",
                "СПб Консерватория — музыковедение"
            ])

        teacher = Teacher(
            full_name=full_name,
            specialization=random.choice(SPECIALIZATIONS),
            email=f"{fake.user_name()}@harmony-school.ru",
            phone=fake.phone_number(),
            experience_years=random.randint(0, 45),
            education=education,
            photo_path=random_teacher_photo(),   # случайный путь из 5 фото
            salary=round(random.uniform(50000, 150000), 2),
            status=random.choice([1, 1, 1, 0]),
            created_at=int(time.time()) - random.randint(0, 365*24*3600),
            updated_at=int(time.time()) - random.randint(0, 30*24*3600)
        )
        teachers.append(teacher)

    db.session.add_all(teachers)
    db.session.commit()
    print(f'✅ Добавлено {count} преподавателей (фото из 5 вариантов).')

def create_gallery(count=100):
    existing = Gallery.query.count()
    if existing >= count:
        print(f'ℹ️ В галерее уже {existing} записей, генерация пропущена.')
        return

    galleries = []
    for i in range(count):
        gallery = Gallery(
            title=fake.sentence(nb_words=3).rstrip('.'),
            description=fake.paragraph(nb_sentences=2),
            file_path=random_gallery_photo(),    # случайный путь из 5 фото
            file_size=random.randint(50000, 5_000_000),
            mime_type=random.choice(['image/jpeg', 'image/png', 'image/webp']),
            width=random.choice([800, 1024, 1280, 1920, 2560]),
            height=random.choice([600, 768, 960, 1080, 1440]),
            category=random.choice(GALLERY_CATEGORIES),
            sort_order=i+1,
            is_published=random.choice([1, 1, 1, 0]),
            uploaded_by=1 if random.random() < 0.7 else None,
            created_at=int(time.time()) - random.randint(0, 180*24*3600),
            updated_at=int(time.time()) - random.randint(0, 60*24*3600)
        )
        galleries.append(gallery)

    db.session.add_all(galleries)
    db.session.commit()
    print(f'✅ Добавлено {count} записей в галерею (фото из 5 вариантов).')

def main():
    print("🔄 Запуск наполнения БД 'music_school'...")
    app = create_app()
    with app.app_context():
        db.create_all()
        print('📁 Таблицы созданы/проверены.')
        create_admin()
        create_teachers(100)
        create_gallery(100)
        print("\n✅ Готово!")
        print(f"📊 Статистика: Users={User.query.count()}, Teachers={Teacher.query.count()}, Gallery={Gallery.query.count()}")

if __name__ == '__main__':
    main()