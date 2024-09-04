# Django Web Project
![Django](https://img.shields.io/badge/Django-4.2.9-brightgreen)
![Celery](https://img.shields.io/badge/Celery-5.2.6-orange)
![Redis](https://img.shields.io/badge/Redis-4.0.2-blue)
## Описание
Этот проект представляет собой интернет-магазин, разработанный на Django, с использованием PostgreSQL в качестве базы данных, Redis для кэширования и Celery для асинхронной отправки почты,. Проект включает в себя аутентификацию пользователей с помощью `django-allauth` и поддержку форм с помощью `django-crispy-forms`.
## Установка
### Предварительные требования
- Docker
- Docker Compose

## Запуск проекта

Для запуска проекта, выполните следующую команду:

```bash
git clone https://github.com/1alexvlad/internet-shop.git

docker-compose up --build