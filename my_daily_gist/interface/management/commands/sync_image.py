from django.core.management.base import BaseCommand, CommandError
from interface.models import *
import uuid

class Command(BaseCommand):
    help = 'Syncs image'

    def handle(self, *args, **options):
        image_url = raw_input("What's the image URL?: ")
        title = raw_input("What's the title?: ")

        if image_url and title:
            img = SocialPost()
            img.description = title
            img.post_id = str(uuid.uuid4()).split("-")[0]
            img.image_url = image_url
            img.post_type = SocialPost.SOCIAL_POST_IMAGE
            img.save()