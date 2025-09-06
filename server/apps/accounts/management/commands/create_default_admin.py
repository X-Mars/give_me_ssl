from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a default admin user (username=admin, password=admin123) if not exists.'

    def handle(self, *args, **options):  # type: ignore[override]
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Default admin user created: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
