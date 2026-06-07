from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse


class LoginRateLimitMiddleware:
    """Small cache-backed rate limiter for the login endpoint."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/login/" and request.method == "POST":
            ip_address = request.META.get("REMOTE_ADDR", "unknown")
            key = f"login-attempts:{ip_address}"
            attempts = cache.get(key, 0) + 1
            cache.set(key, attempts, timeout=300)
            if attempts > 10:
                messages.error(request, "Too many login attempts. Try again in five minutes.")
                return HttpResponse("Too many login attempts.", status=429)
        response = self.get_response(request)
        if request.path == "/login/" and request.method == "POST" and getattr(response, "status_code", 0) in (302, 303):
            cache.delete(f"login-attempts:{request.META.get('REMOTE_ADDR', 'unknown')}")
        return response
