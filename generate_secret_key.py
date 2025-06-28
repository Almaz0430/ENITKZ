#!/usr/bin/env python
"""
Скрипт для генерации безопасного SECRET_KEY для Django.
"""

import secrets
import os
from pathlib import Path
from dotenv import load_dotenv

def generate_secret_key(length=50):
    """Генерирует криптографически стойкий случайный ключ."""
    return secrets.token_urlsafe(length)

def update_env_file(secret_key):
    """Обновляет файл .env с новым SECRET_KEY."""
    env_path = Path('.') / '.env'
    
    # Если файл .env существует, обновляем его
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        
        with open(env_path, 'r') as file:
            lines = file.readlines()
        
        with open(env_path, 'w') as file:
            key_updated = False
            for line in lines:
                if line.startswith('DJANGO_SECRET_KEY='):
                    file.write(f'DJANGO_SECRET_KEY={secret_key}\n')
                    key_updated = True
                else:
                    file.write(line)
            
            if not key_updated:
                file.write(f'\nDJANGO_SECRET_KEY={secret_key}\n')
        
        print(f"SECRET_KEY обновлен в файле .env")
    else:
        # Создаем новый файл .env
        with open(env_path, 'w') as file:
            file.write(f'# Переменные окружения для Django\n')
            file.write(f'DJANGO_SECRET_KEY={secret_key}\n')
            file.write(f'DJANGO_DEBUG=False\n\n')
            file.write(f'# Настройки базы данных\n')
            file.write(f'DATABASE_URL=sqlite:///db.sqlite3\n\n')
            file.write(f'# Настройки безопасности\n')
            file.write(f'ALLOWED_HOSTS=localhost,127.0.0.1\n')
            file.write(f'CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173\n\n')
            file.write(f'# URL фронтенда\n')
            file.write(f'FRONTEND_URL=http://localhost:5173\n')
        
        print(f"Создан новый файл .env с SECRET_KEY")

def main():
    """Основная функция скрипта."""
    print("Генерация нового SECRET_KEY для Django...")
    secret_key = generate_secret_key()
    print(f"\nНовый SECRET_KEY: {secret_key}")
    
    update = input("\nОбновить файл .env с новым SECRET_KEY? (y/n): ").lower()
    if update == 'y':
        update_env_file(secret_key)
    else:
        print("\nДля ручного обновления добавьте следующую строку в файл .env:")
        print(f"DJANGO_SECRET_KEY={secret_key}")

if __name__ == "__main__":
    main() 