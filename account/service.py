from django.core.mail import send_mail


def send(user_email):
    send_mail(
        "Сообщение от shop-internet",
        "Воспользуйся промокодом 'СТАРТ' и получи 30% скидку на покупку.",
        "cinematv2121@gmail.com",
        [user_email],
        fail_silently=False,
    )