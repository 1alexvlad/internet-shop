from website.celery import app

from .service import send_confirmation_email, send_password_reset_email
from django.contrib.auth.models import User


@app.task
def send_registration_email(user_email, user):
    send_confirmation_email(user)


@app.task
def send_password_reset_email_task(user_email, user_id):
    try:
        user = User.objects.get(pk=user_id) 
        send_password_reset_email(user)
    except User.DoesNotExist:
        pass  

