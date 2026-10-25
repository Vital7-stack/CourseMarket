from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest  # Правильный импорт

from .models import Product, Category
from .forms import ContactForm, ProductForm
from .services import get_product_by_id, get_products_by_category


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()[:3]


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner == request.user or request.user.has_perm('catalog.can_unpublish_product'):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("Вы не можете редактировать этот товар")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner == request.user or request.user.has_perm('catalog.can_unpublish_product'):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("Вы не можете удалять этот товар")


class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def product_detail(request, product_id):
    product = get_product_by_id(product_id)
    if not product:
        return render(request, '404.html', status=404)
    return render(request, 'catalog/product_detail.html', {'product': product})


def category_products(request, slug=None, category_id=None):
    if slug:
        category = get_object_or_404(Category, slug=slug)
    elif category_id:
        category = get_object_or_404(Category, id=category_id)
    else:
        return HttpResponseBadRequest("Недостаточно параметров")

    products = get_products_by_category(category.id)
    return render(request, 'catalog/category_products.html', {
        'category': category,
        'products': products
    })