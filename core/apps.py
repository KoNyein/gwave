from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if os.environ.get("DJANGO_SUPERUSER_USERNAME"):
            if not User.objects.filter(username=os.environ["DJANGO_SUPERUSER_USERNAME"]).exists():
                User.objects.create_superuser(
                    username=os.environ["DJANGO_SUPERUSER_USERNAME"],
                    email=os.environ.get("DJANGO_SUPERUSER_EMAIL", ""),
                    password=os.environ["DJANGO_SUPERUSER_PASSWORD"]
                )