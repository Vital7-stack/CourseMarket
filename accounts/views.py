from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Для классов представлений (UpdateView, DetailView) и защиты
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView  # <-- ЭТОГО НЕ ХВАТАЛО
from django.urls import reverse_lazy

from .forms import RegistrationForm, ProfileUpdateForm
from .models import User  # <-- ЭТОГО ТОЖЕ НЕ ХВАТАЛО (чтобы работало model = User)


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


# --- КЛАСС ДЛЯ РЕДАКТИРОВАНИЯ ПРОФИЛЯ (У ТЕБЯ УЖЕ БЫЛ) ---
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        # Защита: редактируем только свой профиль
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён!')
        return super().form_valid(form)


# --- НОВЫЙ КЛАСС ДЛЯ ПРОСМОТРА ПРОФИЛЯ (ЗАЩИЩЁННЫЙ DETAILVIEW) ---
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        # Защита: показываем только профиль текущего пользователя
        return self.request.user


def logout_view(request):
    logout(request)
    return redirect("catalog:home")