from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


# Inline для отображения связи Post-Category
class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1  # Количество пустых форм для добавления


# Настройка отображения постов
class PostAdmin(admin.ModelAdmin):
    # Поля для редактирования (без categories)
    fields = ('author', 'post_type', 'title', 'text', 'rating')

    # Добавляем inline для связи с категориями
    inlines = [PostCategoryInline]

    # Поля в списке
    list_display = ('title', 'author', 'post_type', 'created_at', 'rating')
    list_filter = ('post_type', 'created_at')
    search_fields = ('title', 'text')


# Регистрируем модели
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
