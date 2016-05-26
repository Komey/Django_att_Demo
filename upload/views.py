from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from upload.models import Attachment,KeyValue
from django.template import RequestContext
import os

# Create your views here.
def upload(request):
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            name = uf.cleaned_data['name']
            source = uf.cleaned_data['source']
            try:
                att = Attachment.objects.get(name=name)
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                os.remove(os.path.join(BASE_DIR, att.source.url))
                att.source = source
                att.save()

            except:
                att = Attachment()
                att.name = name
                att.source = source
                att.save()
            return HttpResponseRedirect("/upload")
    else:
        uf = UserForm()
    ur = Attachment.objects.order_by('id')
    return render_to_response('upload.html', {'uf': uf,'ur':ur}, context_instance=RequestContext(request))

class UserForm(forms.Form):
    name = forms.CharField()
    source = forms.FileField()


def setkey(request):
    if request.method == "POST":
        kf = KeyForm(request.POST)
        if kf.is_valid():
            key = kf.cleaned_data['key']
            value = kf.cleaned_data['value']
            try:
                keys = KeyValue.objects.get(key=key)
                keys.value = value
                keys.save()
            except:
                keys = KeyValue()
                keys.key = key
                keys.value = value
                keys.save()
            return HttpResponseRedirect("/key")
    else:
        kf = KeyForm()
    ur = KeyValue.objects.order_by('id')
    return render_to_response('key.html', {'kf': kf,'ur':ur}, context_instance=RequestContext(request))

class KeyForm(forms.Form):
    key = forms.CharField()
    value = forms.CharField()

def download(request):
    name = request.REQUEST.get("name",'')
    ur = Attachment.objects.get(name = name)
    filename = str(ur.source.url)

    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    response = HttpResponse(readFile(filename))
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def getValue(request):
    key = request.REQUEST.get("key", '')
    keys = KeyValue.objects.get(key=key)
    return HttpResponse(keys.value)