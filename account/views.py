from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


from django.contrib.auth.models import User

# Модели и фунции Аутентификации
from django.contrib.auth.models import auth
from django.urls import reverse, reverse_lazy

from cart.models import Cart

from .forms import UserCreateForm, LoginForm, UserUpdateForm

User = get_user_model()


class RegistrationView(CreateView):
    template_name = 'account/register/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('shop:products')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance    

        if user:
            form.save()
            auth.login(self.request, user)

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
                # Удаляем старую аунтификацию сессии
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # Добавляем новую авторизацию пользователя из анонимной сессии
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
        # Отображаем страницу подтверждения удаления
        context = {
            "title": "Удаление аккаунта"
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Удаляем пользователя
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