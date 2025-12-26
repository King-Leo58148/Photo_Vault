<<<<<<< HEAD
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'

class AuthenticatedUserRateThrottle(UserRateThrottle):
    """Throttle authenticated users based on their user ID"""
    scope = 'authenticated_user'
    
    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.id
            }
        return None

class TokenAuthThrottle(UserRateThrottle):
    """Throttle token-authenticated users based on their token"""
    scope = 'token_auth'
    
    def get_cache_key(self, request, view):
        if request.auth:  # Token authentication
            return self.cache_format % {
                'scope': self.scope,
                'ident': str(request.auth)
            }
        return None
=======
from rest_framework.throttling import AnonRateThrottle

class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'
>>>>>>> 1d5b253 (added throttle (rate limit) to prevent login abuse)
