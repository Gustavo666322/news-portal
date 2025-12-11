from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    """Список всех новостей (не статей)"""
    news = Post.objects.filter(post_type='NW').order_by('-created_at')
    return render(request, 'news/list.html', {'news_list': news})

def news_detail(request, news_id):
    """Детальная страница новости"""
    news = get_object_or_404(Post, id=news_id, post_type='NW')
    return render(request, 'news/detail.html', {'news': news})
