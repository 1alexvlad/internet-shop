from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from .tokens import account_activation_token

def generate_activation_link(user):
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return f"http://127.0.0.1:8000/account/confirm/{uid}/{token}/"

def generate_password_reset_link(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return f"http://127.0.0.1:8000/account/reset/{uid}/{token}/"


def send_email(subject, message, user_email):
    send_mail(
        subject,
        message,
        "cinematv2121@gmail.com",
        [user_email],
        fail_silently=False,
    )

def send_confirmation_email(user):
    confirmation_link = generate_activation_link(user)
    subject = 'Подтверждение регистрации'
    message = f"Пожалуйста, подтвердите ваш аккаунт, перейдя по ссылке: {confirmation_link}"
    send_email(subject, message, user.email)


def send_password_reset_email(user):
    reset_link = generate_password_reset_link(user)
    subject = 'Сброс пароля'
    message = f'Пожалуйста, перейдите по ссылке для смены пароля: {reset_link}'
    send_email(subject, message, user.email)
