from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render_to_response, render
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import hashlib
import json
import subprocess
from PIL import Image
import glob
import os

IMG_EXT = "png" #file extension of images that you want to resize

def interface_index(request):
    info = {}
    gists = []

    try:
        gists = requests.get('https://api.github.com/users/six519/gists').json()
    except:
        pass

    paginator = Paginator(gists, settings.MY_DAILY_GIST_PER_PAGE)
    page = request.GET.get('page','')

    try:
        gists = paginator.page(page)
    except PageNotAnInteger:
        gists = paginator.page(1)
    except EmptyPage:
        gists = paginator.page(paginator.num_pages)

    info['gists'] = gists
    info['with_page'] = True

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
            "latitude":"13.939115",
            "longitude":"121.155161",
            "description":"This is where i am living",
            "name":"My House"
        },
        {
            "id":"2",
            "latitude":"13.938758",
            "longitude":"121.153868",
            "description":"Gasoline station on our street",
            "name":"Phoenix"
        },
        {
            "id":"3",
            "latitude":"13.938053",
            "longitude":"121.154968",
            "description":"Kaberks house",
            "name":"Regie"
        }
    ]

    res = HttpResponse(json.dumps(ret), content_type="application/json")

    res['Access-Control-Allow-Origin'] = '*'

    return res

def image_converter(request):
    info = {}

    if request.method == "POST":
        zip_file = request.FILES['zip_file']
        res_width = int(request.POST.get("width", 100))
        res_height = int(request.POST.get("height", 100))
        img_res_tuple = (res_width, res_height,)

        filename, extension = os.path.splitext(zip_file.name)

        destination = open("%s%s" % (settings.MEDIA_ROOT, zip_file.name), 'wb+')

        for chunk in uploaded.chunks():
            destination.write(chunk)

        destination.close()

        unzip = subprocess.Popen("unzip -d %s -o %s" % (filename, zip_file.name), shell=True, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = unzip.communicate()
        unzip.stdout.close()

        needToResizeImages = glob.glob("%s*.%s" % (settings.MEDIA_ROOT, IMG_EXT))


        for needToResizeImage in needToResizeImages:
            imgToResize = Image.open(needToResizeImage)
            imgToResize = imgToResize.convert("RGBA")
            imgToResize.thumbnail(img_res_tuple, Image.ANTIALIAS)
            resizedImage = Image.new('RGBA', img_res_tuple, (255, 255, 255, 0,))
            resizedImage.paste(imgToResize,((img_res_tuple[0] - imgToResize.size[0]) / 2, (img_res_tuple[1] - imgToResize.size[1]) / 2))
            resizedImage.save("%s%s%s" % (settings.MEDIA_ROOT, "resized_", needToResizeImage))

        return HttpResponse('All resized images filename are prefixed with "resized_" and can be viewed at <a href="/media/%s">/media/%s</a>' % (filename, filename))

    return render_to_response('interface/image_converter.html',info,RequestContext(request))

