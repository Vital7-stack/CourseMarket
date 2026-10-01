from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .models import Product
from .forms import ContactForm


class HomeView(ListView):
    """Главная страница: 3 последних товара."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Берём только первые 3 товара — как было в старом FBV
        return Product.objects.all()[:3]


class ProductListView(ListView):
    """Каталог всех товаров."""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """Страница одного товара."""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


class ContactsView(FormView):
    """Страница контактов с формой обратной связи."""
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        # Сохраняем сообщение в БД, как было в старом FBV
        form.save()
        return super().form_valid(form)