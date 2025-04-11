from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

def send_reset_password_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.SITE_URL}/reset-password/{uid}/{token}/"
    subject = 'Password Reset Requested'
    message = f"Click the link below to reset your password:\n{reset_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    