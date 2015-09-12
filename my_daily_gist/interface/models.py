from django.db import models

class SocialPost(models.Model):

    SOCIAL_POST_GIST = 0
    SOCIAL_POST_YOUTUBE = 1

    class Meta:
        db_table = "social_posts"

    description = models.CharField(db_column="description", max_length=255, blank=True)
    post_id = models.CharField(db_column="post_id", max_length=255, blank=True)
    post_type = models.PositiveIntegerField(db_column="post_type", default=SOCIAL_POST_GIST)