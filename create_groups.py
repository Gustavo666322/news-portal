import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortalNew.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post


def create_groups():
    print("=== СОЗДАНИЕ ГРУПП ===")

    # 1. Создаем группу common (обычные пользователи)
    common_group, created = Group.objects.get_or_create(name='common')
    if created:
        print(f"✓ Группа 'common' создана")
    else:
        print(f"✓ Группа 'common' уже существует")

    # 2. Создаем группу authors (авторы)
    authors_group, created = Group.objects.get_or_create(name='authors')
    if created:
        print(f"✓ Группа 'authors' создана")
    else:
        print(f"✓ Группа 'authors' уже существует")

    # 3. Даем права группе authors
    content_type = ContentType.objects.get_for_model(Post)

    # Права для постов
    permissions = [
        'add_post',  # создание постов
        'change_post',  # редактирование постов
        'delete_post',  # удаление постов
    ]

    added_count = 0
    for perm_codename in permissions:
        try:
            perm = Permission.objects.get(codename=perm_codename, content_type=content_type)
            authors_group.permissions.add(perm)
            print(f"✓ Право '{perm_codename}' добавлено группе 'authors'")
            added_count += 1
        except Permission.DoesNotExist:
            print(f"✗ Право '{perm_codename}' не найдено")

    print(f"\n=== ИТОГ ===")
    print(f"Группа 'common': {common_group}")
    print(f"Группа 'authors': {authors_group}")
    print(f"Добавлено прав для authors: {added_count}")

    # 4. Сохраняем изменения
    authors_group.save()
    print("\nГруппы успешно настроены!")


if __name__ == "__main__":
    create_groups()