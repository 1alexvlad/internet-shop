from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'account'

urlpatterns = [
    # Регистрация
    path('register/', views.RegistrationView.as_view(), name='register'),
    
    # Вход и выход
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Dashboard
    path('dashboard/', views.DashboardUserView.as_view(), name='dashboard'),
    path('profile-management/', views.UserProfileView.as_view(), name='profile-management'),
    path('delete-user/', views.DeleteUserView.as_view(), name='delete-user'),
]