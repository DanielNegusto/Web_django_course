from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, ProfileUpdateForm
from django.contrib.messages import success


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('catalog:catalog')  # Перенаправление на каталог

    def form_valid(self, form):
        # Сначала сохраняем пользователя через форму
        user = form.save()

        # Авторизуем пользователя сразу после регистрации
        login(self.request, user)

        # Отправляем приветственное письмо
        send_mail(
            'Добро пожаловать!',
            'Спасибо за регистрацию в нашем сервисе!',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        # Добавляем сообщение об успешной регистрации
        success(self.request, 'Регистрация прошла успешно!')

        # После успешной регистрации отправляем пользователя на страницу каталога
        return redirect(self.success_url)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('catalog:catalog')

    def get_object(self, queryset=None):
        return self.request.user  # Получаем текущего авторизованного пользователя

    def form_valid(self, form):
        # Отправляем сообщение об успешном обновлении профиля
        success(self.request, 'Ваш профиль был успешно обновлен!')
        return super().form_valid(form)
