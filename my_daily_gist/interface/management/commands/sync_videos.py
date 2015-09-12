from django.core.management.base import BaseCommand, CommandError
from interface.models import *
import feedparser

class Command(BaseCommand):
    help = 'Syncs youtube videos'

    def handle(self, *args, **options):
        print "Fetching youtube videos..."
        videos = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCCdNET-0VecBzTLMB3m6PrA")
        cnt = 0

        for i, video in enumerate(videos["entries"]):
            print "Reading youtube video # %s" % (i + 1)

            vid_id = video["id"].split(":")[2]
            vid = SocialPost.objects.filter(post_id=vid_id, post_type=SocialPost.SOCIAL_POST_YOUTUBE)

            if vid.count() == 0:
                cnt += 1
                new_video = SocialPost()
                new_video.description = video["title"]
                new_video.post_id = vid_id
                new_video.post_type = SocialPost.SOCIAL_POST_YOUTUBE
                new_video.save()

        print "Number of new youtube video saved: %s" % cnt