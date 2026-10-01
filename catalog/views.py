from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ContactForm


def home(request):
    # Единственное изменение: берём только первые 3 товара
    products = Product.objects.all()[:3]
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ContactForm()
    return render(request, 'catalog/contacts.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})