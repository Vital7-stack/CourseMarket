from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Главная
    path('', views.HomeView.as_view(), name='home'),

    # Каталог товаров
    path('products/', views.ProductListView.as_view(), name='product_list'),

    # Детальная страница товара
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Контакты
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]