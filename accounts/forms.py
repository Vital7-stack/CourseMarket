from django import forms
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

        # Проверка сложности пароля
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