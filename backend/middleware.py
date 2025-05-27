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