from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница (для ссылки "Главная" в меню)
    path('', views.home, name='home'),

    # Каталог товаров (для ссылки "Каталог" в меню)
    path('products/', views.product_list, name='product_list'),

    # Детальная страница товара
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    # Контакты
    path('contacts/', views.contacts, name='contacts'),
]