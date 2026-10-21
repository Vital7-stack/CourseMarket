from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import BlogPost


class BlogListView(ListView):
    """Список блоговых записей — только опубликованные."""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Фильтруем: только is_published=True
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Детальная страница статьи + увеличение счётчика просмотров."""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # Берём объект стандартным способом
        obj = super().get_object(queryset)
        # Увеличиваем счётчик просмотров
        obj.views_count += 1
        # Сохраняем только поле views_count (эффективнее, чем save() без параметров)
        obj.save(update_fields=['views_count'])
        return obj


class BlogCreateView(CreateView):
    """Создание новой статьи."""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    """Редактирование статьи."""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        # После редактирования — на страницу этой же статьи
        return reverse('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Удаление статьи."""
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')