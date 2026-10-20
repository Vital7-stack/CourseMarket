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

    # Создание товара (ВНИМАНИЕ: стоит ДО <int:pk>/, чтобы не перехватилось)
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),

    # Редактирование товара
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),

    # Удаление товара
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Контакты
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]