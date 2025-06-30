# ENITKZ - Образовательный портал

## Русская версия

### Описание проекта
Образовательный портал для казахстанских вузов с функциями регистрации университетов, управления образовательными программами, аккредитациями, публикациями и программами мобильности.

### Технологии
- Backend: Django, Django REST Framework
- База данных: PostgreSQL
- Аутентификация: Django Session Auth, Token Auth
- Документация API: drf-spectacular (Swagger, Redoc)
- Безопасность: CSRF защита, WhiteNoise, Django Security Headers

### Установка и запуск (локально)

1. **Клонирование репозитория:**
```bash
git clone https://github.com/Almaz0430/ENITKZ.git
cd ENITKZ
```

2. **Создание виртуального окружения:**
```bash
python -m venv venv
venv\Scripts\activate  # для Windows
# или
source venv/bin/activate  # для Linux/macOS
```

3. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

4. **Настройка переменных окружения:**
```bash
copy env.example .env
# Отредактируйте файл .env, установив необходимые значения
```

5. **Применение миграций:**
```bash
python manage.py migrate
```

6. **Создание суперпользователя:**
```bash
python manage.py createsuperuser
```

7. **Сбор статических файлов:**
```bash
python manage.py collectstatic
```

8. **Запуск сервера разработки:**
```bash
python manage.py runserver
```

После этого сайт будет доступен по адресу http://127.0.0.1:8000/

## English version

### Project Description
Educational portal for Kazakhstan universities with features for university registration, educational programs management, accreditations, publications, and mobility programs.

### Technologies
- Backend: Django, Django REST Framework
- Database: PostgreSQL
- Authentication: Django Session Auth, Token Auth
- API Documentation: drf-spectacular (Swagger, Redoc)
- Security: CSRF protection, WhiteNoise, Django Security Headers

### Installation and Setup (Local)

1. **Clone the repository:**
```bash
git clone https://github.com/Almaz0430/ENITKZ.git
cd ENITKZ
```

2. **Create a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # for Windows
# or
source venv/bin/activate  # for Linux/macOS
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
copy env.example .env
# Edit the .env file with your settings
```

5. **Apply migrations:**
```bash
python manage.py migrate
```

6. **Create a superuser:**
```bash
python manage.py createsuperuser
```

7. **Collect static files:**
```bash
python manage.py collectstatic
```

8. **Run the development server:**
```bash
python manage.py runserver
```

After these steps, the site will be available at http://127.0.0.1:8000/ 