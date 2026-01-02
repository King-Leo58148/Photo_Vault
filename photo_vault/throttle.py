
from rest_framework.throttling import UserRateThrottle

class loginRateThrottle(UserRateThrottle):
    scope = 'login'

class signupRateThrottle(UserRateThrottle):
    scope = 'signup'
