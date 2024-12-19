from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, auth
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetDoneView
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages


from cart.models import Cart

from .forms import LoginForm, UserCreateForm, UserUpdateForm, PasswordResetForm, EmailChangeForm
from .tasks import send_registration_email, send_password_reset_email_task
from .service import send_confirmation_email, send_password_reset_email
from .tokens import account_activation_token


User = get_user_model()


class RegistrationView(CreateView):
    template_name = 'account/register/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('shop:products')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        auth.login(self.request, user)

        messages.success(self.request, 'Письмо для подтверждения аккаунта было отправлено на указанную почту.')
        
        confirmation_link = send_confirmation_email(user)
        send_registration_email.delay(user.email, confirmation_link)
        

        if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context  


class UserLoginView(LoginView):
    template_name = 'account/login/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('shop:products')

    def get_success_url(self) -> str:
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('shop:products')    
    
    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

        return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context   


class DashboardUserView(LoginRequiredMixin, TemplateView):
    template_name = 'account/dashboard/dashboard.html'
    login_url = 'account:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Аккаунт'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'account/dashboard/profile-management.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('shop:products')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        return context
    

class DeleteUserView(LoginRequiredMixin, View):
    template_name = 'account/dashboard/account-delete.html'
    login_url = 'account:login'
    success_url = reverse_lazy('shop:products')

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Удаление аккаунта"
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return redirect(self.success_url)
    


def logout_user(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        if key == 'session_key':
            continue
        del request.session[key]
    auth.logout(request)
    return redirect('shop:products')


class ConfirmAccountView(View):
    template_name = 'account/register/confirmation_invalid.html'

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('shop:products')
        else:
            context = {
                'title': 'Ошибка подтверждения'
            }
            return render(request, self.template_name, context)

    

class PasswordChangeView(View):
    template_name = 'account/login/password_change.html'
    form_class = 'EmailChangeForm'


    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_password_reset_email_task.delay(user.email, user.id)          
                messages.success(request, "Ссылка для сброса пароля была отправлена на ваш email.")
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким email не найден')
        else:
            messages.error(request, "Пожалуйста, введите корректный адрес электронной почты.")

        return render(request, self.template_name, {'form': form})



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/login/password_reset_confirm.html'
    form_class = PasswordResetForm

    def post(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Пользователь не найден.")
            user = self.form_invalid(None)        

        form = self.get_form()
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль успешно сменен.")
            return redirect('shop:products')
        else:
            messages.error(request, "Пароли не совпадают.")
        
        return self.form_invalid(form)