from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post, Subscription
from django.contrib.auth.models import Group, User


@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        try:
            common_group = Group.objects.get(name='common')
            instance.groups.add(common_group)
            instance.save()
        except Group.DoesNotExist:
            pass


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type == Post.ARTICLE:  # Исправлено!
        # Получаем всех подписчиков категорий статьи
        for category in instance.categories.all():
            subscriptions = Subscription.objects.filter(category=category)
            for subscription in subscriptions:
                send_new_article_email(subscription.user, instance)


def send_new_article_email(user, article):
    """Отправка письма о новой статье с обработкой ошибок"""
    if not user.email:  # Проверка email
        return

    subject = f'Новая статья в категории {article.categories.first().name}'

    try:
        message = render_to_string('new_article.html', {
            'user': user,
            'article': article,
        })

        send_mail(
            subject,
            '',
            'noreply@newportal.com',
            [user.email],
            html_message=message,
            fail_silently=False,
        )
        print(f"Уведомление отправлено пользователю {user.username}")
    except Exception as e:
        print(f"Ошибка отправки уведомления для {user.username}: {e}")


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Приветственное письмо с обработкой ошибок"""
    if created and instance.email:  # Проверка email
        subject = 'Добро пожаловать в News Portal!'

        try:
            message = render_to_string('welcome.html', {
                'user': instance,
            })

            send_mail(
                subject,
                '',
                'noreply@newportal.com',
                [instance.email],
                html_message=message,
                fail_silently=False,
            )
            print(f"Приветственное письмо отправлено пользователю {instance.username}")
        except Exception as e:
            print(f"Ошибка отправки приветственного письма для {instance.username}: {e}")