from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from rest_framework_simplejwt.exceptions import TokenError


def generate_email_verification_token(user):
    """
    Generates a JWT token that will be used to verify email.
    The token contains the user's email and an expiration time.
    """
    refresh = RefreshToken.for_user(user)
    refresh.set_exp(lifetime=timedelta(minutes=15))  
    return str(refresh.access_token)


def verify_email_token(token):
    """
    Verifies the JWT token and returns the user's email if valid.
    """
    try:
        token_obj = RefreshToken(token)
        return token_obj['email']  # Return the email from the token
    except TokenError:
        return None