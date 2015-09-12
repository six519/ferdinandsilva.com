from interface.models import SocialPost

def mysite_contexts(request):

	return {
		"SOCIAL_POST_GIST": SocialPost.SOCIAL_POST_GIST,
		"SOCIAL_POST_YOUTUBE": SocialPost.SOCIAL_POST_YOUTUBE
	}