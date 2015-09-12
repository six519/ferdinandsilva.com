from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Syncs github gists'

    def handle(self, *args, **options):
        pass