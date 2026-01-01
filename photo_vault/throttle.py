from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'


class AuthenticatedUserRateThrottle(UserRateThrottle):
    """Throttle authenticated users based on their user ID"""
    scope = 'authenticated_user'

    def get_cache_key(self, request, view):
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            return self.cache_format % {
                'scope': self.scope,
                'ident': user.id
            }
        return None


class TokenAuthThrottle(UserRateThrottle):
    """Throttle token-authenticated users based on their token"""
    scope = 'token_auth'

    def get_cache_key(self, request, view):
        token = getattr(request, 'auth', None)
        if token:
            ident = getattr(token, 'key', None) or str(token)
            return self.cache_format % {
                'scope': self.scope,
                'ident': ident
            }
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            return self.cache_format % {
                'scope': self.scope,
                'ident': user.id
            }
        return None
