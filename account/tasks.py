from website.celery import app

from .service import send_confirmation_email, send_password_reset_email
from django.contrib.auth.models import User
from celery.exceptions import SoftTimeLimitExceeded


@app.task(time_limit=120, soft_time_limit=100)
def send_registration_email(user_email, user_id):
    try:
        user = User.objects.get(pk=user_id)
        send_confirmation_email(user_email, user)
    except SoftTimeLimitExceeded:
        print("Мягкий лимит времени превышен. Завершение задачи.")



@app.task(time_limit=120, soft_time_limit=100)
def send_password_reset_email_task(user_email, user_id):
    try:
        user = User.objects.get(pk=user_id) 
        send_password_reset_email(user)
    except User.DoesNotExist:
        pass
    except SoftTimeLimitExceeded:
        print("Мягкий лимит времени превышен. Завершение задачи.")

