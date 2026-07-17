from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserProfileForm
from users.forms import UserRegisterForm, UserLoginForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()

        send_mail(
            subject='Добро пожаловать в eCatalog!',
            message=f'Здравствуйте, {user.email}! Вы успешно зарегистрировались на нашем портале.',
            from_email=None,  # Будет использован DEFAULT_FROM_EMAIL из settings
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')


# Профиль пользователя
class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
