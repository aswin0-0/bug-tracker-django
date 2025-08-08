from django.apps import AppConfig


class BuggedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bugged'
