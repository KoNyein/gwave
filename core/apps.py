
                
                
                from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        if os.environ.get("RAILWAY_ENVIRONMENT"):
            User = get_user_model()
            if not User.objects.filter(username=os.environ["DJANGO_SUPERUSER_USERNAME"]).exists():
                User.objects.create_superuser(
                    username=os.environ["DJANGO_SUPERUSER_USERNAME"],
                    email=os.environ["DJANGO_SUPERUSER_EMAIL"],
                    password=os.environ["DJANGO_SUPERUSER_PASSWORD"],
                )
                