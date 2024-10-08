from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

class RegistrationViewTest(TestCase):

    def test_register_valid_data(self):
        """Тест автоматического входа пользователя после регистрации"""
        form_data = {'username': 'Ivan', 'password1': 'sdfksdASIDOFAWI234', 'password2': 'sdfksdASIDOFAWI234', }

        temlate_user = self.client.get(reverse('account:register'))
        self.assertTemplateUsed(temlate_user, 'account/register/register.html')

        response = self.client.post(reverse('account:register'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username='Ivan').exists())
    
    def test_register_redirects_to_success_url(self):
        """Тест перенаправление пользователя после успешной регистрации"""
        form_data = {'username': 'Ivan', 'password1': 'sdfksdASIDOFAWI234', 'password2': 'sdfksdASIDOFAWI234', }
        response = self.client.post(reverse('account:register'), data=form_data)
        self.assertRedirects(response, reverse('shop:products'))

    def test_user_is_logged_in_after_registration(self):
        """Тест автоматического входа пользователя после регистрации"""
        form_data = {'username': 'Ivan', 'password1': 'sdfksdASIDOFAWI234', 'password2': 'sdfksdASIDOFAWI234', }
        response = self.client.post(reverse('account:register'), data=form_data)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    
class UserLoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_valid_data(self):
        """Тест успешного входа с валидными данными."""
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('account:login'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)


    def test_login_invalid_data(self):
        """Тест невалидации формы с некорректными данными."""
        form_data = {'username': 'wronguser', 'password': 'wrongpassword'}
        response = self.client.post(reverse('account:login'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    
class DashboardUserViewTesst(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassWORD123')

    def test_dashboard_view_reqiured_login(self):
        """Тест, что предствление требуют авторизации"""
        response = self.client.get(reverse('account:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/?next=/account/dashboard/')

    def test_dashboard_view_with_authenticated_user(self):
        """Тест на отображение предствления для авторизированного пользователя"""
        self.client.login(username = 'testuser', password='testpassWORD123')
        response = self.client.get(reverse('account:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/dashboard/dashboard.html')


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='sdfkjFKJLAFJ4230409')
            

    def test_profile_view_requires_login(self):
        """Тест, что представления требуют авторизации"""
        response = self.client.get(reverse('account:profile-management'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/?next=/account/profile-management/')

    def test_profile_view_with_authenticated_user(self):
        """Тест на отображение предствления для авторизированного пользователя"""
        self.client.login(username='testuser', password='sdfkjFKJLAFJ4230409')
        response = self.client.get(reverse('account:profile-management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/dashboard/profile-management.html')

    def test_profile_view_form_valid(self):
        """Тест валидации формы с корректными данными."""
        form_data = {
            'username': 'newusername',
        }
        self.client.login(username='testuser', password='sdfkjFKJLAFJ4230409')
        response = self.client.post(reverse('account:profile-management'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.url, reverse('shop:products'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')


class DeleteUserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='sdfkjFKJLAFJ4230409')

    def test_delete_user_view_requires_login(self):
        """Тест, что представление требует авторизации"""
        response = self.client.get(reverse('account:delete-user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account:login')}?next={reverse('account:delete-user')}")

    def test_delete_user_view_with_authenticated_user(self):
        """Тест отображения представления для аутентифицированного пользователя"""
        self.client.login(username='testuser', password='sdfkjFKJLAFJ4230409')
        response = self.client.get(reverse('account:delete-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/dashboard/account-delete.html')

    def test_delte_user(self):
        """Удаление пользователя"""
        self.client.login(username='testuser', password='sdfkjFKJLAFJ4230409')
        response = self.client.post(reverse('account:delete-user'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.url, reverse('shop:products'))
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class LogoutUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='sdfkjFKJLAFJ4230409')

    def test_logout_user(self):
        """Тест выхода из системы"""
        self.client.login(username='testuser', password='sdfkjFKJLAFJ4230409')
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:products'))
