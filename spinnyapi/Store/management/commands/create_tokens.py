from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create tokens for existing users'

    def handle(self, *args, **options):
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Token created for user: {user.username}'))
