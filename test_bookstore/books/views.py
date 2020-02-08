from django.shortcuts import render
from . import views
from django.views import generic, View
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Document, Book
from .forms import DocumentForm
from django.db.models import Q
from django.views.generic import TemplateView, ListView


def index(request):
    documents = Document.objects.all()
    print(request)
    return render(request, 'index.html', {'documents': documents})

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fs.delete('onix.xml')#make sure the previous file is deleted
        filename = fs.save('onix.xml', myfile) #use the same name for all uploaded onix files. To ease the check.
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

def onixfile(request):
    documents = Document.objects.all()
    print(request)
    return render(request, 'onixfile.html', {'documents': documents})

def detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'detail.html', {'book': book})

def process_Onix(request):
    message=''
    color = 'red' # red if error message and green if success
    if request.method=='POST':
        fs=FileSystemStorage()
        if fs.exists('onix.xml'):
            #Code to parse goes here
            message='Successfully processed the Onix file.'
            color='green'
        
        
        else:
            message='No file to process.'
            color='red'

    context={
        'message':message,
        'color':color
        }
    return render(request,'process.html', context)                                                                                             

class SearchResultsView(ListView):
    model = Book
    template_name = 'search.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(authors__icontains=query)
        )
        return object_list
        
    
