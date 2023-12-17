from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Display tokens for all users'

    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                token = Token.objects.get(user=user)
                self.stdout.write(self.style.SUCCESS(f'Token for {user.username}: {token.key}'))
            except Token.DoesNotExist:
                self.stdout.write(self.style.SUCCESS(f'No token found for {user.username}'))
