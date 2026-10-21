from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('blogs/', include('blog.urls')),          # обрати внимание: у тебя тут 'blogs/', а в menu.html — 'blog:blog_list'
    path('accounts/', include('accounts.urls')),
    # ← ДОБАВЛЕНО: маршрут для выхода
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)