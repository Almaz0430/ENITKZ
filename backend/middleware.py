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
        
        # 1. Content-Security-Policy (CSP)
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; form-action 'self';"
        
        # 2. X-Frame-Options (защита от clickjacking)
        response['X-Frame-Options'] = 'SAMEORIGIN'
        
        # 3. X-Content-Type-Options (предотвращение MIME-sniffing)
        response['X-Content-Type-Options'] = 'nosniff'
        
        # 4. Strict-Transport-Security (HSTS)
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # 5. Удаление X-Powered-By
        if 'X-Powered-By' in response:
            del response['X-Powered-By']
        
        # 6. Cache-Control
        if not response.get('Cache-Control'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        
        # 7. Referrer-Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response 