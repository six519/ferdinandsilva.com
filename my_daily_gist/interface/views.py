from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render_to_response, render
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
import requests

def interface_index(request):
    info = {}
    gists = []

    try:
        gists = requests.get('https://api.github.com/users/six519/gists').json()
    except:
        pass

    info['gists'] = gists

    return render_to_response('interface/index.html',info,RequestContext(request))

def interface_view(request, id):
    info = {}
    gists = []
    exists = False

    try:
        gists = requests.get('https://api.github.com/users/six519/gists').json()

        for gist in gists:
            if str(gist['id']) == str(id):
                 gists = [gist]
                 exists = True
                 break

    except:
        pass

    if not exists:
        return redirect('interface_index')

    info['gists'] = gists

    return render_to_response('interface/index.html',info,RequestContext(request))