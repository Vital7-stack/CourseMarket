from django import forms
from django.core.exceptions import ValidationError

from .models import ContactMessage, Product


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'Ваше имя',
            'email': 'Email',
            'message': 'Сообщение',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


# === НОВОЕ ДЛЯ ДОМАШКИ 3 ===

# Константа — список запрещённых слов (Задание 1, критерий: "список вынесен в константу")
FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(forms.ModelForm):
    """Форма создания и редактирования товара с валидацией и стилизацией."""

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        labels = {
            'name': 'Название товара',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена (₽)',
        }

    # --- Задание 3: Стилизация через __init__ ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Проходим по всем полям и добавляем Bootstrap-классы
        for field_name, field in self.fields.items():
            if field_name == 'image':
                # Для файла — другой класс
                field.widget.attrs.update({'class': 'form-control', 'type': 'file'})
            elif field_name == 'is_published':
                # Чекбокс — как checkbox (на будущее, если поле появится)
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                # Все остальные — обычный input/textarea/select
                field.widget.attrs.update({'class': 'form-control'})

        # Описание делаем повыше
        if 'description' in self.fields:
            self.fields['description'].widget.attrs.update({'rows': 4})

    # --- Задание 1: Валидация запрещённых слов ---
    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        name_lower = name.lower()  # Регистр игнорируется
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(
                    f'Слово «{word}» запрещено использовать в названии продукта.'
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        description_lower = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise ValidationError(
                    f'Слово «{word}» запрещено использовать в описании продукта.'
                )
        return description

    # --- Задание 2: Валидация цены (не может быть отрицательной) ---
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError(
                'Цена не может быть отрицательной. Укажите положительное значение.'
            )
        return price