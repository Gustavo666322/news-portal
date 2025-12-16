import django_filters
from django import forms
from .models import Post


class NewsFilter(django_filters.FilterSet):
    """Фильтр для поиска новостей"""
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название...'})
    )

    author = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя автора...'})
    )

    date_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Позже даты',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Выберите дату...'
            }
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'date_after']