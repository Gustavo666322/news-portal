from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Post, Subscription


def send_weekly_email(user, articles):
    """Отправка еженедельной рассылки конкретному пользователю"""
    if not user.email:  # Проверка наличия email
        return

    subject = f'Еженедельная подборка статей за неделю'

    # Получаем категории пользователя
    user_categories = Subscription.objects.filter(user=user).values_list('category__name', flat=True)

    message = render_to_string('weekly_digest.html', {
        'user': user,
        'articles': articles,
        'categories': ', '.join(user_categories)
    })

    try:
        send_mail(
            subject,
            '',  # Текстовое сообщение пустое, используем html_message
            'noreply@newportal.com',
            [user.email],
            html_message=message,
            fail_silently=False,
        )
        print(f"Еженедельная рассылка отправлена пользователю {user.username}")
    except Exception as e:
        print(f"Ошибка отправки еженедельной рассылки для {user.username}: {e}")


@shared_task
def send_weekly_digest():
    """Основная задача для еженедельной рассылки"""
    week_ago = timezone.now() - timedelta(days=7)

    # Получаем всех пользователей с подписками
    users_with_subs = User.objects.filter(
        subscription__isnull=False
    ).distinct()

    for user in users_with_subs:
        # Получаем категории пользователя
        user_categories = Subscription.objects.filter(user=user).values_list('category', flat=True)

        # Статьи за неделю в категориях пользователя
        articles = Post.objects.filter(
            post_type=Post.ARTICLE,
            created_at__gte=week_ago,
            categories__id__in=user_categories
        ).distinct()

        if articles.exists():
            send_weekly_email(user, articles)

    return f"Еженедельная рассылка отправлена {users_with_subs.count()} пользователям"