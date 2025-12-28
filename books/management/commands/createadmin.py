from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import os

class Command(BaseCommand):
    help = "Create a superuser using environment variables"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.ERROR("Missing environment variables"))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Superuser already exists"))
            return

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_superuser=True,
            is_staff=True,
        )

        self.stdout.write(self.style.SUCCESS("Superuser created successfully"))