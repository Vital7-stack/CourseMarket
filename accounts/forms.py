from django import forms
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2", "avatar", "phone", "country"]
        labels = {
            "email": "Email",
            "username": "Имя пользователя",
            "avatar": "Аватар",
            "phone": "Номер телефона",
            "country": "Страна",
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")

        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                raise ValidationError(e)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # Только данные для редактирования. Паролей здесь нет.
        fields = ['email', 'username', 'phone', 'country', 'avatar']
        labels = {
            'username': 'Имя пользователя',
            'phone': 'Номер телефона',
            'country': 'Страна',
            'avatar': 'Аватар',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7...'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }