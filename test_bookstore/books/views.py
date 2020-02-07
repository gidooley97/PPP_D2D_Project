from django.shortcuts import render
from . import views
from django.views import generic, View

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Document
from .forms import DocumentForm

def index(request):
    documents = Document.objects.all()
    print(request)
    return render(request, 'index.html', {'documents': documents})

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

def onixfile(request):
    documents = Document.objects.all()
    print(request)
    return render(request, 'onixfile.html', {'documents': documents})
def process_Onix(request):
    context={'file_is_found':'False'}
    if request.method=='POST':
        #call the parsing code here.
        context= {'file_is_found':'True'}
    
    return render(request, 'process.html',context)


