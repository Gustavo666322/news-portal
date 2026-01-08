import os

# Базовый путь для лог-файлов
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # Для DEBUG в консоль (простой)
        'console_debug': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
        # Для WARNING в консоль (с pathname)
        'console_warning': {
            'format': '{asctime} {levelname} {pathname} {message}',
            'style': '{',
        },
        # Для ERROR/CRITICAL в консоль (с exc_info)
        'console_error': {
            'format': '{asctime} {levelname} {pathname} {message}\n{exc_info}',
            'style': '{',
        },
        # Для general.log
        'general': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        # Для errors.log
        'error': {
            'format': '{asctime} {levelname} {message} {pathname}\n{exc_info}',
            'style': '{',
        },
        # Для security.log
        'security': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        # Для email
        'email': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        # Консольный обработчик для DEBUG
        'console_debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_debug',
            'filters': ['require_debug_true'],
        },
        # Консольный обработчик для WARNING
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning',
            'filters': ['require_debug_true'],
        },
        # Консольный обработчик для ERROR
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'console_error',
            'filters': ['require_debug_true'],
        },
        # Файл general.log
        'file_general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'general.log'),
            'formatter': 'general',
            'filters': ['require_debug_false'],
        },
        # Файл errors.log
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'errors.log'),
            'formatter': 'error',
        },
        # Файл security.log
        'file_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'security.log'),
            'formatter': 'security',
        },
        # Почтовый обработчик
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'email',
            'filters': ['require_debug_false'],
            'include_html': False,
        },
    },
    'loggers': {
        # Основной логгер Django - ВСЕ сообщения
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_error', 'file_general'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Логгеры для errors.log и email
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Логгер безопасности
        'django.security': {
            'handlers': ['file_security'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}