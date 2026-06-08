from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Create a superuser from environment variables when one does not already exist."

    def handle(self, *args, **options):
        email = settings.CMPES_ADMIN_EMAIL
        password = settings.CMPES_ADMIN_PASSWORD
        full_name = settings.CMPES_ADMIN_FULL_NAME
        reset_password = settings.CMPES_ADMIN_RESET_PASSWORD

        if not email or not password:
            self.stdout.write("CMPES admin env vars not set; skipping superuser creation.")
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "full_name": full_name,
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created or reset_password:
            user.full_name = full_name
            user.role = User.Role.ADMIN
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(password)
            user.save()
            action = "Created" if created else "Updated password for"
            self.stdout.write(self.style.SUCCESS(f"{action} superuser {email}."))
        else:
            self.stdout.write(f"Superuser {email} already exists; leaving password unchanged.")
