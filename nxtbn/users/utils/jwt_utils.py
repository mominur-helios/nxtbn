from datetime import datetime, timedelta, timezone
import jwt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


JWT_SECRET_KEY = settings.NXTBN_JWT_SETTINGS['SECRET_KEY']
JWT_ALGORITHM = settings.NXTBN_JWT_SETTINGS['ALGORITHM']
ACCESS_TOKEN_EXPIRATION_SECONDS = settings.NXTBN_JWT_SETTINGS['ACCESS_TOKEN_EXPIRATION_SECONDS']
REFRESH_TOKEN_EXPIRATION_SECONDS = settings.NXTBN_JWT_SETTINGS['REFRESH_TOKEN_EXPIRATION_SECONDS']


# Generate a JWT token
def generate_jwt_token(user, expiration_seconds):
    """Generate a JWT token for a given user with specified expiration."""
    exp = datetime.now(timezone.utc) + timedelta(seconds=expiration_seconds)
    payload = {
        "user_id": user.id,
        "exp": exp,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# Generate access and refresh tokens
def generate_access_token(user):
    return generate_jwt_token(user, ACCESS_TOKEN_EXPIRATION_SECONDS)

def generate_refresh_token(user):
    return generate_jwt_token(user, REFRESH_TOKEN_EXPIRATION_SECONDS)

# Verify a JWT token
def verify_jwt_token(token):
    """Verify a JWT token and return the associated user."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user = User.objects.get(id=payload["user_id"])
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ObjectDoesNotExist):
        return None