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
from lxml import etree
from .process_onix import process_data
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator



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
    color = 'green' # red if error message and green if success
    path= "documents/onix.xml"
    # root= load_onix_file(path)
    # data=process_data(root)[:5]
    # for dt in data:
    #     print(dt.series)
    if request.method=='POST':
        
        fs=FileSystemStorage()
        if fs.exists('onix.xml'):
            #Code to parse goes here
            root= load_onix_file(path)
            data=process_data(root)
            #Store data in the database
            for dt in data:          
                try:
                    book = Book.objects.get(isbn_13=dt.isbn_13)
                    #print("Updating")
                    book.title =dt.title
                    book.authors=dt.authors
                    book.subtitle = dt.subtitle
                    book.series=dt.series
                    book.volume=dt.volume
                    book.desc = dt.desc
                    book.book_formats= dt.book_formats
                    book.sale_flag = dt.sale_flag
                    book.save()
                
                except Book.DoesNotExist:
                    #print("inserting")
                    book = Book.objects.create(title=dt.title, authors=dt.authors, isbn_13=dt.isbn_13,
                    subtitle = dt.subtitle, series=dt.series, volume=dt.volume,
                    desc=dt.desc, book_formats=dt.book_formats,
                    sale_flag=dt.sale_flag)

            message='Successfully processed the Onix file.'
            color='green'
            books = Book.objects.all()
            for bk in books:
                print(bk)
            fs.delete('onix.xml') #delete onix file
        else:
            message='No file to process.'
            color='red'

    context={
        'message':message,
        'color':color
        }
    return render(request,'process.html', context)   

def load_onix_file(path):
    context=''
    try:
        context = etree.parse(path)
    except:
        print("unable to parse onix file.")
        
    return context                                                                                          

class SearchResultsView(ListView):
    model = Book
    template_name = 'search.html'
    paginate_by = 20

    def get_queryset(self): 
        object_list = []
        query = self.request.GET.get('q')
        if query is None:
            query = "a"
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(authors__icontains=query) | Q(isbn_13__icontains=query) | Q(subtitle__icontains=query)
            | Q(series__icontains=query) | Q(volume__icontains=query) | Q(desc__icontains=query) | Q(book_formats__icontains=query)
            | Q(sale_flag__icontains=query)
        )
        return object_list
        
    