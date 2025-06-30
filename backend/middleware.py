import re
from django.conf import settings

class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.csrf_exempt_urls = [re.compile(url) for url in settings.CSRF_EXEMPT_URLS]

    def __call__(self, request):
        if any(pattern.match(request.path_info) for pattern in self.csrf_exempt_urls):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Установка заголовков безопасности с более мягкими настройками для разработки
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "img-src 'self' data: https://*.unsplash.com https://*.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "connect-src 'self' http://127.0.0.1:8000 https://web-production-eeb3.up.railway.app",
            "frame-src 'self' https://www.google.com",
            "form-action 'self'"
        ]
        
        response['Content-Security-Policy'] = "; ".join(csp_directives)
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        if 'X-Powered-By' in response:
            del response['X-Powered-By']
        
        if not response.get('Cache-Control'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response 