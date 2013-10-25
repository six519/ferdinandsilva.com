from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render_to_response, render
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
import requests
import hashlib
import json

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
    info['site_title'] = gists[0]['description']

    return render_to_response('interface/index.html',info,RequestContext(request))

def sha1_view(request):

    sha1 = hashlib.sha1()
    txt = request.GET.get('txt','')
    ret = ""

    if txt != "":
        sha1.update(txt)
        ret = str(sha1.hexdigest())

    return HttpResponse(ret)

def json_test(request):

    ret = [
        {
            "id":"1",
            "longitude":"13.939",
            "latitude":"121.155",
            "description":"This is where i am living",
            "name":"My House"
        },
        {
            "id":"2",
            "longitude":"13.938",
            "latitude":"121.153",
            "description":"Gasoline station on our street",
            "name":"Phoenix"
        },
        {
            "id":"3",
            "longitude":"13.938",
            "latitude":"121.154",
            "description":"Kaberks house",
            "name":"Regie"
        }
    ]

    return HttpResponse(json.dumps(ret), content_type="application/json")



