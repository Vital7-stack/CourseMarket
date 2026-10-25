from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Главная
    path('', views.HomeView.as_view(), name='home'),

    # Каталог товаров
    path('products/', views.ProductListView.as_view(), name='product_list'),

    # Детальная страница товара (для админки / авторизованных)
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Создание товара
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),

    # Редактирование товара
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),

    # Удаление товара
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Контакты
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    # Публичная страница продукта (кэш на уровне сервиса)
    path('catalog/product/<int:product_id>/', views.product_detail, name='product_detail_public'),

    # Публичная страница категории (кэш на уровне сервиса)
    # Добавляем два URL: один для ID, другой для slug
    path('catalog/category/<int:category_id>/', views.category_products, name='category_products_by_id'),
    path('catalog/category/<slug:slug>/', views.category_products, name='category_products_by_slug'),
]