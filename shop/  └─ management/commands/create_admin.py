from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create admin user if not exists"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@gwave.site",
                password=os.environ.get("ADMIN_PASSWORD")
            )
            self.stdout.write("Admin user created")
        else:
            self.stdout.write("Admin already exists")