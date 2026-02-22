
                
                from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        if os.environ.get("RAILWAY_ENVIRONMENT"):
            from django.contrib.auth import get_user_model
            User = get_user_model()

            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    "admin",
                    "admin@gwave.site",
                    os.environ.get("ADMIN_PASSWORD")
                )
                