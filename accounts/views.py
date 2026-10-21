from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm

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
