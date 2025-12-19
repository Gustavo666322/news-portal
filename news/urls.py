from django.urls import path
from . import views
from .views import become_author

urlpatterns = [
    # Главная страница со списком новостей
    path('', views.NewsListView.as_view(), name='news_list'),

    # Детальная страница новости
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),

    # Поиск новостей
    path('search/', views.news_search, name='news_search'),

    # Новости: создание, редактирование, удаление
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='news_delete'),

    # Статьи: создание, редактирование, удаление
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.PostUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.PostUpdateView.as_view(), name='article_delete'),

    # Стать автором
    path('become-author/', become_author, name='become_author'),

    # Управление подписками (НОВЫЕ URL)
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/subscribe/', views.subscribe_category, name='subscribe_category'),
    path('category/<int:category_id>/unsubscribe/', views.unsubscribe_category, name='unsubscribe_category'),
]
