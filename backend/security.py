"""
Модуль с дополнительными настройками безопасности для Django проекта.
"""

# Настройки безопасности для Django
SECURITY_SETTINGS = {
    # Настройки защиты от XSS
    'CSP_DEFAULT_SRC': ("'self'",),
    'CSP_SCRIPT_SRC': ("'self'",),
    'CSP_STYLE_SRC': ("'self'",),
    'CSP_IMG_SRC': ("'self'", "data:"),
    'CSP_FONT_SRC': ("'self'",),
    'CSP_CONNECT_SRC': ("'self'",),
    'CSP_FRAME_ANCESTORS': ("'none'",),
    'CSP_FORM_ACTION': ("'self'",),
    
    # Настройки защиты от Clickjacking
    'X_FRAME_OPTIONS': 'SAMEORIGIN',
    
    # Настройки защиты от MIME-sniffing
    'X_CONTENT_TYPE_OPTIONS': 'nosniff',
    
    # Настройки HSTS
    'HSTS_INCLUDE_SUBDOMAINS': True,
    'HSTS_PRELOAD': True,
    'HSTS_MAX_AGE': 31536000,  # 1 год
    
    # Настройки Referrer Policy
    'REFERRER_POLICY': 'strict-origin-when-cross-origin',
    
    # Настройки Cookie
    'SESSION_COOKIE_SECURE': True,
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'CSRF_COOKIE_SECURE': True,
    'CSRF_COOKIE_HTTPONLY': True,
    'CSRF_COOKIE_SAMESITE': 'Lax',
    
    # Другие настройки безопасности
    'SECURE_BROWSER_XSS_FILTER': True,
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'SECURE_SSL_REDIRECT': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
}

# Рекомендации по безопасности
SECURITY_RECOMMENDATIONS = [
    "1. Регулярно обновляйте зависимости проекта",
    "2. Используйте HTTPS для всех соединений",
    "3. Проводите регулярный аудит безопасности",
    "4. Ограничьте доступ к административным интерфейсам",
    "5. Используйте многофакторную аутентификацию где возможно",
    "6. Настройте мониторинг и логирование действий пользователей",
    "7. Регулярно создавайте резервные копии данных",
    "8. Используйте защиту от DDoS-атак",
    "9. Проверяйте все пользовательские входные данные",
    "10. Не храните чувствительные данные в коде или конфигурационных файлах"
]

def apply_security_settings(settings_dict):
    """
    Применяет настройки безопасности к словарю настроек Django.
    
    Args:
        settings_dict: Словарь настроек Django
    
    Returns:
        Обновленный словарь настроек
    """
    for key, value in SECURITY_SETTINGS.items():
        if key in settings_dict:
            settings_dict[key] = value
    return settings_dict

def get_security_headers():
    """
    Возвращает словарь с заголовками безопасности для HTTP-ответов.
    
    Returns:
        Словарь с заголовками безопасности
    """
    return {
        'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; form-action 'self';",
        'X-Frame-Options': 'SAMEORIGIN',
        'X-Content-Type-Options': 'nosniff',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
    } 