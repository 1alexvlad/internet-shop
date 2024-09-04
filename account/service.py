from django.core.mail import send_mail


def send(user_email):
    send_mail(
        "Вы подписаны на рассылку",
        "Мы будем присылать письма",
        "cinematv2121@gmail.com",
        [user_email],
        fail_silently=False,
    )