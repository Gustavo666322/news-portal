from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Post
from .forms import PostForm
from .filters import NewsFilter


# ========== СПИСОК НОВОСТЕЙ (С ПАГИНАЦИЕЙ) ==========
class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        """Возвращаем только новости (не статьи)"""
        return Post.objects.filter(post_type=Post.NEWS).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все новости'

        # Пагинация с номерами лишь ближайших страниц
        paginator = context['paginator']
        page_obj = context['page_obj']
        current_page = page_obj.number

        # Вычисляем диапазон страниц для отображения
        num_pages = paginator.num_pages

        # Показываем 3 страницы до и после текущей
        start_page = max(current_page - 3, 1)
        end_page = min(current_page + 3, num_pages)

        # Гарантируем, что показываем хотя бы 5 страниц если возможно
        if end_page - start_page < 4 and num_pages > 5:
            if current_page <= 3:
                end_page = min(5, num_pages)
            else:
                start_page = max(num_pages - 4, 1)

        context['page_range'] = range(start_page, end_page + 1)
        context['first_page'] = 1
        context['last_page'] = num_pages
        context['has_previous'] = page_obj.has_previous()
        context['has_next'] = page_obj.has_next()

        return context


# ========== ПОИСК НОВОСТЕЙ (ФИЛЬТРАЦИЯ) ==========
def news_search(request):
    """Представление для поиска новостей с фильтрацией"""
    # Получаем все новости (не статьи)
    news_list = Post.objects.filter(post_type=Post.NEWS).order_by('-created_at')

    # Применяем фильтры
    news_filter = NewsFilter(request.GET, queryset=news_list)
    filtered_news = news_filter.qs

    # Пагинация
    paginator = Paginator(filtered_news, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Вычисляем диапазон страниц для отображения
    current_page = page_obj.number
    num_pages = paginator.num_pages

    start_page = max(current_page - 3, 1)
    end_page = min(current_page + 3, num_pages)

    # Гарантируем, что показываем хотя бы 5 страниц если возможно
    if end_page - start_page < 4 and num_pages > 5:
        if current_page <= 3:
            end_page = min(5, num_pages)
        else:
            start_page = max(num_pages - 4, 1)

    context = {
        'title': 'Поиск новостей',
        'filter': news_filter,
        'news_list': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'page_range': range(start_page, end_page + 1),
        'first_page': 1,
        'last_page': num_pages,
        'search_performed': bool(request.GET),
    }

    return render(request, 'news/news_search.html', context)


# ========== СОЗДАНИЕ НОВОСТИ ==========
class NewsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        """Устанавливаем тип поста как "новость" перед сохранением"""
        post = form.save(commit=False)
        post.post_type = Post.NEWS  # Устанавливаем тип "новость"
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание новости'
        return context


# ========== СОЗДАНИЕ СТАТЬИ ==========
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        """Устанавливаем тип поста как "статья" перед сохранением"""
        post = form.save(commit=False)
        post.post_type = Post.ARTICLE  # Устанавливаем тип "статья"
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание статьи'
        return context


# ========== РЕДАКТИРОВАНИЕ ПОСТА ==========
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Запись успешно обновлена!')
        return reverse_lazy('news_list')


# ========== УДАЛЕНИЕ ПОСТА ==========
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Запись успешно удалена!')
        return super().delete(request, *args, **kwargs)


# ========== ДЕТАЛЬНАЯ СТРАНИЦА НОВОСТИ ==========
class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        """Показываем только новости"""
        return Post.objects.filter(post_type=Post.NEWS)