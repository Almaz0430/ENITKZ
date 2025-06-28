#!/usr/bin/env python
"""
Скрипт для проверки безопасности Django-проекта.
Проверяет настройки безопасности, заголовки и другие аспекты безопасности.
"""

import os
import sys
import requests
import json
import re
from urllib.parse import urlparse
import django
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла, если он существует
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print("Переменные окружения загружены из файла .env")
else:
    print("Файл .env не найден. Рекомендуется создать его для хранения секретных настроек.")

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings

# Цвета для вывода в консоль
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message):
    """Печатает заголовок."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_result(message, success):
    """Печатает результат проверки."""
    if success:
        print(f"{Colors.OKGREEN}[✓] {message}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}[✗] {message}{Colors.ENDC}")

def print_warning(message):
    """Печатает предупреждение."""
    print(f"{Colors.WARNING}[!] {message}{Colors.ENDC}")

def print_info(message):
    """Печатает информацию."""
    print(f"{Colors.OKBLUE}[i] {message}{Colors.ENDC}")

def check_env_variables():
    """Проверяет наличие и настройку переменных окружения."""
    print_header("Проверка переменных окружения")
    
    # Проверка SECRET_KEY
    secret_key = os.environ.get('DJANGO_SECRET_KEY', '')
    is_default_key = not secret_key or 'django-insecure' in secret_key
    print_result("SECRET_KEY установлен через переменную окружения", bool(secret_key) and not is_default_key)
    
    # Проверка DEBUG
    debug = os.environ.get('DJANGO_DEBUG', '').lower()
    print_result("DEBUG установлен через переменную окружения", debug in ['true', 'false'])
    if debug == 'true':
        print_warning("DEBUG=True в продакшн-окружении может быть небезопасно")
    
    # Проверка ALLOWED_HOSTS
    allowed_hosts = os.environ.get('ALLOWED_HOSTS', '')
    print_result("ALLOWED_HOSTS установлен через переменную окружения", bool(allowed_hosts))
    if allowed_hosts:
        hosts = allowed_hosts.split(',')
        print_info(f"ALLOWED_HOSTS: {', '.join(hosts)}")
        print_result("ALLOWED_HOSTS не содержит '*'", '*' not in hosts)
    
    # Проверка DATABASE_URL
    db_url = os.environ.get('DATABASE_URL', '')
    print_result("DATABASE_URL установлен", bool(db_url))
    
    # Проверка FRONTEND_URL
    frontend_url = os.environ.get('FRONTEND_URL', '')
    print_result("FRONTEND_URL установлен", bool(frontend_url))

def check_django_settings():
    """Проверяет настройки безопасности Django."""
    print_header("Проверка настроек безопасности Django")
    
    # Проверка DEBUG
    print_result("DEBUG выключен", not getattr(settings, 'DEBUG', True))
    
    # Проверка SECRET_KEY
    secret_key = getattr(settings, 'SECRET_KEY', '')
    is_default_key = 'django-insecure' in secret_key
    print_result("SECRET_KEY не является стандартным", not is_default_key)
    
    # Проверка ALLOWED_HOSTS
    allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
    print_result("ALLOWED_HOSTS не содержит '*'", '*' not in allowed_hosts)
    
    # Проверка CSRF
    print_result("CSRF защита включена", getattr(settings, 'CSRF_COOKIE_SECURE', False))
    print_result("CSRF cookie HttpOnly", getattr(settings, 'CSRF_COOKIE_HTTPONLY', False))
    print_result("CSRF cookie SameSite", getattr(settings, 'CSRF_COOKIE_SAMESITE', '') in ['Lax', 'Strict'])
    
    # Проверка сессий
    print_result("SESSION cookie secure", getattr(settings, 'SESSION_COOKIE_SECURE', False))
    print_result("SESSION cookie HttpOnly", getattr(settings, 'SESSION_COOKIE_HTTPONLY', False))
    print_result("SESSION cookie SameSite", getattr(settings, 'SESSION_COOKIE_SAMESITE', '') in ['Lax', 'Strict'])
    
    # Проверка HSTS
    print_result("HSTS включен", getattr(settings, 'SECURE_HSTS_SECONDS', 0) > 0)
    print_result("HSTS включает поддомены", getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False))
    print_result("HSTS preload", getattr(settings, 'SECURE_HSTS_PRELOAD', False))
    
    # Проверка других настроек безопасности
    print_result("XSS фильтр браузера включен", getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False))
    print_result("Content-Type nosniff включен", getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False))
    print_result("X-Frame-Options настроен", getattr(settings, 'X_FRAME_OPTIONS', '') in ['DENY', 'SAMEORIGIN'])
    print_result("Referrer-Policy настроен", hasattr(settings, 'REFERRER_POLICY'))
    
    # Проверка CORS
    cors_allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
    cors_allow_all = getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False)
    print_result("CORS не разрешает все домены", not cors_allow_all)
    print_info(f"CORS разрешенные домены: {', '.join(cors_allowed_origins)}")

def check_headers(url):
    """Проверяет заголовки безопасности на указанном URL."""
    print_header(f"Проверка заголовков безопасности на {url}")
    
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        headers = response.headers
        
        # Проверка CSP
        csp = headers.get('Content-Security-Policy', '')
        print_result("Content-Security-Policy установлен", bool(csp))
        if csp:
            print_info(f"CSP: {csp}")
            print_result("CSP не содержит 'unsafe-inline'", 'unsafe-inline' not in csp)
            print_result("CSP не содержит 'unsafe-eval'", 'unsafe-eval' not in csp)
        
        # Проверка X-Frame-Options
        x_frame = headers.get('X-Frame-Options', '')
        print_result("X-Frame-Options установлен", bool(x_frame))
        if x_frame:
            print_info(f"X-Frame-Options: {x_frame}")
        
        # Проверка X-Content-Type-Options
        x_content_type = headers.get('X-Content-Type-Options', '')
        print_result("X-Content-Type-Options установлен", x_content_type.lower() == 'nosniff')
        
        # Проверка Strict-Transport-Security
        hsts = headers.get('Strict-Transport-Security', '')
        print_result("Strict-Transport-Security установлен", bool(hsts))
        if hsts:
            print_info(f"HSTS: {hsts}")
            print_result("HSTS включает поддомены", 'includeSubDomains' in hsts)
            
            # Проверка max-age
            max_age_match = re.search(r'max-age=(\d+)', hsts)
            if max_age_match:
                max_age = int(max_age_match.group(1))
                print_result("HSTS max-age >= 1 год", max_age >= 31536000)
            else:
                print_result("HSTS max-age установлен", False)
        
        # Проверка Referrer-Policy
        referrer = headers.get('Referrer-Policy', '')
        print_result("Referrer-Policy установлен", bool(referrer))
        if referrer:
            print_info(f"Referrer-Policy: {referrer}")
        
        # Проверка Cache-Control
        cache_control = headers.get('Cache-Control', '')
        print_result("Cache-Control установлен", bool(cache_control))
        if cache_control:
            print_info(f"Cache-Control: {cache_control}")
        
        # Проверка X-Powered-By
        x_powered_by = headers.get('X-Powered-By', '')
        print_result("X-Powered-By не раскрывает информацию", not bool(x_powered_by))
        
        # Проверка Server
        server = headers.get('Server', '')
        print_result("Server не раскрывает детальную информацию", not bool(server) or server == 'Server')
        
    except requests.exceptions.RequestException as e:
        print_warning(f"Ошибка при проверке заголовков: {e}")

def check_cookies(url):
    """Проверяет настройки cookies на указанном URL."""
    print_header(f"Проверка cookies на {url}")
    
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        cookies = response.cookies
        
        if not cookies:
            print_info("Cookies не установлены")
            return
        
        for cookie in cookies:
            print_info(f"Cookie: {cookie.name}")
            print_result(f"Cookie {cookie.name} имеет secure", cookie.secure)
            print_result(f"Cookie {cookie.name} имеет httponly", cookie.has_nonstandard_attr('httponly'))
            
            # Проверка SameSite
            samesite = None
            for attr in cookie._rest.keys():
                if attr.lower() == 'samesite':
                    samesite = cookie._rest[attr]
            
            print_result(f"Cookie {cookie.name} имеет SameSite", samesite in ['Lax', 'Strict'])
            if samesite:
                print_info(f"SameSite: {samesite}")
    
    except requests.exceptions.RequestException as e:
        print_warning(f"Ошибка при проверке cookies: {e}")

def main():
    """Основная функция скрипта."""
    print_header("Проверка безопасности Django-проекта")
    
    # Проверка переменных окружения
    check_env_variables()
    
    # Проверка настроек Django
    check_django_settings()
    
    # Проверка заголовков и cookies на локальном сервере
    url = input("\nВведите URL для проверки заголовков и cookies (например, http://localhost:8000): ")
    if url:
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = f"http://{url}"
        
        check_headers(url)
        check_cookies(url)
    
    print_header("Проверка завершена")
    print_info("Рекомендации по безопасности:")
    print_info("1. Регулярно обновляйте зависимости проекта")
    print_info("2. Используйте HTTPS для всех соединений")
    print_info("3. Проводите регулярный аудит безопасности")
    print_info("4. Ограничьте доступ к административным интерфейсам")
    print_info("5. Используйте многофакторную аутентификацию где возможно")
    print_info("6. Настройте мониторинг и логирование действий пользователей")
    print_info("7. Регулярно создавайте резервные копии данных")
    print_info("8. Используйте защиту от DDoS-атак")
    print_info("9. Проверяйте все пользовательские входные данные")
    print_info("10. Не храните чувствительные данные в коде или конфигурационных файлах")

if __name__ == "__main__":
    main() 