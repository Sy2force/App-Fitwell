from django.shortcuts import redirect
from django.urls import resolve, Resolver404

class OnboardingMiddleware:
    """
    Middleware to redirect non-onboarded users to the onboarding flow.
    Uses URL names to be robust to i18n.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URL names that don't require onboarding
        self.exempt_url_names = [
            'home',
            'login',
            'register',
            'logout',
            'password_reset',
            'password_reset_done',
            'password_reset_confirm',
            'password_reset_complete',
            'legal',
            'onboarding_welcome',
            'onboarding_step1',
            'onboarding_step2',
            'onboarding_step3',
            'set_language', # For i18n switcher
        ]
        
        # Path prefixes always exempt (Admin, API, Static)
        self.exempt_prefixes = [
            '/admin/',
            '/api/',
            '/static/',
            '/media/',
            '/i18n/',
        ]
    
    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user is not onboarded
            if not request.user.is_onboarded:
                path = request.path_info
                
                # 1. Check Prefixes
                if any(path.startswith(prefix) for prefix in self.exempt_prefixes):
                    return self.get_response(request)
                
                # 2. Check URL Name
                try:
                    resolver_match = resolve(path)
                    url_name = resolver_match.url_name
                    
                    if url_name in self.exempt_url_names:
                        return self.get_response(request)
                        
                except Resolver404:
                    pass # 404s will be handled by Django later
                
                # If we're here, the URL is protected and user is not onboarded
                return redirect('onboarding_welcome')
        
        response = self.get_response(request)
        return response
