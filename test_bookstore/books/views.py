from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from django.views import generic, View
from django.views.generic import TemplateView, ListView
from django import template
from . import views
from .models import Document, Book
from .forms import DocumentForm
from .process_onix import process_data
from lxml import etree
from urllib.parse import urlencode

#index.html, otherwise know as our home page
def index(request):
    documents = Document.objects.all()
    print(request)
    return render(request, 'index.html', {'documents': documents})

#simple_upload.html , upload onix file page, allows you to choose onix file then process
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

#onixfile.html, onix file management page, allows you to naviage to uploading onix file or processing the current one that is uploaded
def onixfile(request):
    documents = Document.objects.all()
    print(request)
    return render(request, 'onixfile.html', {'documents': documents})


#detail.html, this is the book detail page 
def detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'detail.html', {'book': book})

#process.html, actually performs the process 
def process_Onix(request):
    message=''
    color = 'green' # red if error message and green if success
    path= "documents/onix.xml"

    if request.method=='POST':
        
        fs=FileSystemStorage()
        if fs.exists('onix.xml'):
            root= load_onix_file(path)
            if root:
                data=process_data(root)
                #Store data in the database
                for dt in data:          
                    try:
                        book = Book.objects.get(isbn_13=dt.isbn_13)
                        book.title =dt.title
                        book.authors=dt.authors
                        book.subtitle = dt.subtitle
                        book.series=dt.series
                        book.volume=dt.volume
                        book.desc = dt.desc
                        book.book_formats= dt.book_formats
                        book.sale_flag = dt.sale_flag
                        book.language = dt.language
                        book.price = dt.price
                        book.save()
                
                    except Book.DoesNotExist:
                        book = Book.objects.create(title=dt.title, authors=dt.authors, isbn_13=dt.isbn_13,
                        subtitle = dt.subtitle, series=dt.series, volume=dt.volume,
                        desc=dt.desc, book_formats=dt.book_formats, language=dt.language, price=dt.price,
                        sale_flag=dt.sale_flag)

                message='Successfully processed the Onix file.'
                color='green'
            else:
                message='Unable to process file. Invalid file.'
                color='red'
            fs.delete('onix.xml') #delete onix file
        else:
            message='No file to process.'
            color='red'

    context={
        'message':message,
        'color':color
        }
    return render(request,'process.html', context)   

#adds functionality for loading onix file
def load_onix_file(path):
    context=''
    try:
        context = etree.parse(path)
    except:
        print("unable to parse onix file.")
        
    return context                                                                                          

#search.html, displays results for query, pagenated by 20
class SearchResultsView(ListView):
    model = Book
    template_name = 'search.html'
    paginate_by = 20 #change to add/remove pages
    

    
    def get_queryset(self): 
        object_list = []
        title_list = []
        other_list = []
        query = self.request.GET.get('s_bar')
        if query is None:
            query = "abcdefhijklmnopqrstuvwxyz"
        title_list = Book.objects.filter(Q(title__icontains=query))
        other_list = Book.objects.filter(Q(authors__icontains=query) | Q(isbn_13__icontains=query) | Q(subtitle__icontains=query)
            | Q(series__icontains=query) | Q(volume__icontains=query) | Q(desc__icontains=query) | Q(book_formats__icontains=query)
            | Q(sale_flag__icontains=query))

        for x in title_list:
            object_list.append(x)
        for x in other_list:
            object_list.append(x)
        return object_list
 
    