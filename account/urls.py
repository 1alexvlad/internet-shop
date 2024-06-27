from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    # Регистрация и верификация
    path('register/', views.register_user, name='register'),
    path('email-verification/', views.email_verification, name='email-verification'),
    
    # Вход и выход
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_user, name='dashboard'),
    path('profile-management/', views.profile_user, name='profile-management'),
    path('delete-user/', views.delete_user, name='delete-user'),
]