from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse

# Миксин для защиты страниц
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product
from .forms import ContactForm, ProductForm


class HomeView(ListView):
    """Главная страница: 3 последних товара."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()[:3]


class ProductListView(ListView):
    """Каталог всех товаров (публичная страница)."""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Страница одного товара (только для авторизованных)."""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    # login_url УДАЛЁН: Django берёт его из settings.py (LOGIN_URL)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового товара (только для авторизованных)."""
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара (только для авторизованных)."""
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def get_success_url(self):
        # После редактирования — на страницу этого товара
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара (только для авторизованных)."""
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class ContactsView(FormView):
    """Страница контактов с формой обратной связи (публичная)."""
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)