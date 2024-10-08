from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase

from ..forms import UserCreateForm, UserUpdateForm

User = get_user_model()


class UserCreateFormTest(TestCase):
    def test_user_create_form_valid(self):
        """Тест успешного создания пользователя с валидными данными"""
        form_data = {
            'username': 'Ivan',
            'password1': 'sdfksdASIDOFAWI234',
            'password2': 'sdfksdASIDOFAWI234',
        }
        form = UserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'Ivan')
        self.assertTrue(user.check_password('sdfksdASIDOFAWI234'))

    def test_user_create_form_invalid(self):
        """Тест на валидацию формы без username"""
        form_data = {
            'username': '',
            'password1': 'sdfksdASIDOFAWI234',
            'password2': 'sdfksdASIDOFAWI234',
        }
        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
    def test_user_creation_form_different_password(self):
        """Тест на валидацию формы с несовпадающими паролями"""
        form_data = {
            'username': 'Ivan',
            'password1': 'dASIDOFAWI234',
            'password2': 'sdfksdASIDOFAWI234',
        }
        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class LoginFormTest(TestCase):
    def test_login_form_valid(self):
        """Тест успешной валидации формы с корректными данными."""
        self.user = User.objects.create_user(username='testuser', password='sdfksdASIDOFAWI234')
        form_data = {
            'username': 'testuser',
            'password': 'sdfksdASIDOFAWI234'
        }
        form = AuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        """Тест невалидации формы с некорректными данными"""
        form_data = {
            'username': '',
            'password': '',
        }
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='sdfksdASIDOFAWI234')

    def test_form_valid_data(self):
        """Тест на успешное изменение username"""
        form_data = {'username': 'newusername'}
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

    def test_form_invalid_data(self):
        """Тест на некоректные данные в username"""
        form_data = {'username': ''}
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
