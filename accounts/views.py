from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Для UpdateView и защиты страниц
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .forms import RegistrationForm, ProfileUpdateForm


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=True)

            # Отправка приветственного письма
            send_mail(
                subject="Добро пожаловать в CourseMarket!",
                message=f"Привет, {user.username}! Ваш аккаунт успешно создан.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            login(request, user)
            return redirect("catalog:home")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "catalog:home")
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


# === ЭТОТ КЛАСС ЗАМЕНЯЕТ ФУНКЦИЮ profile_update_view ===
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')
    # login_url не нужен, так как в settings.py уже есть LOGIN_URL = 'accounts:login'

    def get_object(self):
        # Автоматически подставляет текущего пользователя как instance
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён!')
        return super().form_valid(form)
# =========================================================


def logout_view(request):
    logout(request)
    return redirect("catalog:home")