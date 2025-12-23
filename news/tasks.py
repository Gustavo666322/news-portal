from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Post, Subscription

@shared_task
def send_notifications_to_subscribers(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return f"Post {post_id} не найден"

    categories = post.categories.all()
    subscribers = User.objects.filter(
        subscription__category__in=categories
    ).distinct()

    for user in subscribers:
        if user.email:
            subject = f'Новая запись в категории {", ".join([cat.name for cat in categories])}'
            message = render_to_string('email/new_post_notification.html', {
                'user': user,
                'post': post,
                'categories': categories,
            })
            send_mail(
                subject,
                '',
                'noreply@newportal.com',
                [user.email],
                html_message=message,
                fail_silently=False,
            )

    return f"Уведомления отправлены {subscribers.count()} подписчикам"




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
    week_ago = timezone.now() - timedelta(days=7)
    users_with_subs = User.objects.filter(
        subscription__isnull=False
    ).distinct()

    for user in users_with_subs:
        user_categories = Subscription.objects.filter(
            user=user
        ).values_list('category', flat=True)

        articles = Post.objects.filter(
            created_at__gte=week_ago,
            categories__id__in=user_categories
        ).distinct()

        if articles.exists() and user.email:
            message = render_to_string('email/weekly_digest.html', {
                'user': user,
                'articles': articles,
            })
            send_mail(
                'Еженедельная подборка новостей',
                '',
                'noreply@newportal.com',
                [user.email],
                html_message=message,
                fail_silently=False,
            )

    return f"Еженедельная рассылка отправлена {users_with_subs.count()} пользователям"