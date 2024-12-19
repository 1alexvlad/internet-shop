from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    path('dashboard/', views.DashboardUserView.as_view(), name='dashboard'),
    path('profile-management/', views.UserProfileView.as_view(), name='profile-management'),
    path('delete-user/', views.DeleteUserView.as_view(), name='delete-user'),

    path('confirm/<uidb64>/<token>/', views.confirm_account, name='confirm_account'),

    path('password-change/', views.password_change, name='password_change'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),

]