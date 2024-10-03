from website.celery import app

from .service import send


@app.task
def send_email(user_email):
    send(user_email)
