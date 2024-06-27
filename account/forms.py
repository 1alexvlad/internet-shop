from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django import forms 

from django.forms.widgets import PasswordInput, TextInput


User = get_user_model()


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs) -> None:
        super(CreateUserForm,self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Your Email Address'
        self.fields['email'].required = True
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''

    # Проверяем email 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists() and len(email) > 254:
            raise forms.forms.ValidationError('Емейл адрес уже зарегистрирован или слишком длинный')
        
        return email

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs) -> None:
        super(UserUpdateForm,self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Your Email Address'
        self.fields['email'].required = True



    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ('password1', 'password2')