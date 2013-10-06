#!/usr/bin/env python

import requests

gists = requests.get('https://api.github.com/users/six519/gists')

for gist in gists.json():
	print "%s: %s" % (gist['id'], gist['description'])