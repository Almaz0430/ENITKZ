"""
Модуль настроек безопасности
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
    
    'X_FRAME_OPTIONS': 'SAMEORIGIN',
    'X_CONTENT_TYPE_OPTIONS': 'nosniff',
    
    'HSTS_INCLUDE_SUBDOMAINS': True,
    'HSTS_PRELOAD': True,
    'HSTS_MAX_AGE': 31536000,
    
    'REFERRER_POLICY': 'strict-origin-when-cross-origin',
    
    'SESSION_COOKIE_SECURE': True,
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'CSRF_COOKIE_SECURE': True,
    'CSRF_COOKIE_HTTPONLY': True,
    'CSRF_COOKIE_SAMESITE': 'Lax',
    
    'SECURE_BROWSER_XSS_FILTER': True,
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'SECURE_SSL_REDIRECT': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
}

def apply_security_settings(settings_dict):
    """Применяет настройки безопасности"""
    for key, value in SECURITY_SETTINGS.items():
        if key in settings_dict:
            settings_dict[key] = value
    return settings_dict

def get_security_headers():
    """Возвращает словарь с заголовками безопасности"""
    return {
        'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; form-action 'self';",
        'X-Frame-Options': 'SAMEORIGIN',
        'X-Content-Type-Options': 'nosniff',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
    } 