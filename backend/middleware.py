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
        
        # Установка заголовков безопасности
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; form-action 'self';"
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        if 'X-Powered-By' in response:
            del response['X-Powered-By']
        
        if not response.get('Cache-Control'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response 