from django.core.management.base import BaseCommand, CommandError
from interface.models import *
import requests

class Command(BaseCommand):
    help = 'Syncs github gists'

    def handle(self, *args, **options):
        print "Fetching gists..."
        gists = requests.get('https://api.github.com/users/six519/gists').json()
        gists.reverse()

        cnt = 0
        for i, gist in enumerate(gists):
            print "Reading gist # %s" % (i + 1)
            gst = SocialPost.objects.filter(post_id=gist["id"], post_type=SocialPost.SOCIAL_POST_GIST)

            if gst.count() == 0:
                cnt += 1
                new_gist = SocialPost()
                new_gist.description = gist["description"]
                new_gist.post_id = gist["id"]
                new_gist.save()

        print "Number of new gists saved: %s" % cnt