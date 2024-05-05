from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from nxtbn.users.utils.jwt_utils import verify_jwt_token
class CsrfExemptSessionAuthentication(SessionAuthentication):
    '''
        Security Warning: Don't use this in production environment.
        The class is aim to git rid of CSRF token during development and api test using different tools.
        We can ignore in production, coz, we dont need to SessionWiseAuthenitcation in production as we are using JWT.
        Strongly prohibitted..
    '''
    def enforce_csrf(self, request):
        pass



class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user = verify_jwt_token(token)
            if user:
                return (user, None)
            raise AuthenticationFailed("Invalid or expired token")
        return None
