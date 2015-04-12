from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from vote.models import Status


class Command(BaseCommand):
    help = 'Adds a voter, creating a User object as needed'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, **options):
        email = options['email']

        # If the user does not already exist, add one.
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create user with the name, email, and password all set to `email`
            u = User.objects.create_user(email, email, email)
        
        # If the status object doesn't exist, add one for the user.
        try:
            status = Status.objects.get(user=u)
        except Status.DoesNotExist:
            status = Status()
            status.user = u
            status.save()
