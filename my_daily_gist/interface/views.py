from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render_to_response, render
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from interface.models import *
from .util import *
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
    posts = SocialPost.objects.filter()

    paginator = Paginator(posts, settings.MY_DAILY_GIST_PER_PAGE)
    page = request.GET.get('page','')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except Exception as e:
        print "The error is: %s" % str(e)

    info['posts'] = posts
    info['with_page'] = True

    return render_to_response('interface/index.html',info,RequestContext(request))

def interface_view(request, id):
    info = {}
    posts = SocialPost.objects.filter(post_id=str(id))

    if posts.count() == 0:
        return redirect('interface_index')

    info['posts'] = posts
    info['site_title'] = posts[0].description

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
        zip_full_path = "%s%s" % (settings.MEDIA_ROOT, zip_file.name)

        destination = open(zip_full_path, 'wb+')

        for chunk in zip_file.chunks():
            destination.write(chunk)

        destination.close()

        new_dir = "%s%s" % (settings.MEDIA_ROOT, filename)

        try:
            os.mkdir(new_dir)
            os.chmod(new_dir, 0777)
        except:
            pass

        unzip = subprocess.Popen("unzip -d %s -o %s" % (new_dir, zip_full_path), shell=True, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = unzip.communicate()
        unzip.stdout.close()

        needToResizeImages = glob.glob("%s%s/*.%s" % (settings.MEDIA_ROOT, filename, IMG_EXT))


        for needToResizeImage in needToResizeImages:
            imgToResize = Image.open(needToResizeImage)
            imgToResize = imgToResize.convert("RGBA")
            imgToResize.thumbnail(img_res_tuple, Image.ANTIALIAS)
            resizedImage = Image.new('RGBA', img_res_tuple, (255, 255, 255, 0,))
            resizedImage.paste(imgToResize,((img_res_tuple[0] - imgToResize.size[0]) / 2, (img_res_tuple[1] - imgToResize.size[1]) / 2))
            
            imgFname = os.path.basename(needToResizeImage)
            imgFullPath = "%s%s/%s%s" % (settings.MEDIA_ROOT, filename, "resized_", imgFname)

            resizedImage.save(imgFullPath)

            try:
                os.chmod(imgFullPath, 0777)
            except:
                pass

        tar_file = subprocess.Popen("tar -cvf %s.tar -C %s ." % (new_dir, new_dir), shell=True, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = tar_file.communicate()
        tar_file.stdout.close()

        try:
            os.chmod("%s.tar" % new_dir, 0777)
        except:
            pass

        return HttpResponse('All resized images filename are prefixed with "resized_" and can be viewed at <a href="/media/%s.tar">/media/%s.tar</a>' % (filename, filename))

    return render_to_response('interface/image_converter.html',info,RequestContext(request))

