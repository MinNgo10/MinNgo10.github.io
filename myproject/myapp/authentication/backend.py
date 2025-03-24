from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug(f"Attempting to authenticate user: {username}")

        try:
            user = get_user_model().objects.get(username=username)
            logger.debug(f"User found: {user.username}")
        except get_user_model().DoesNotExist:
            logger.warning(f"User not found: {username}")
            return None

        if user.password == password:
            logger.debug(f"Password correct for user: {username}")
            return user
        else:
            logger.warning(f"Incorrect password for user: {username}")
            return None
