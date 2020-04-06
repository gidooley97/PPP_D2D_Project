from django.shortcuts import render

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

from .search_checkmate import search
from lxml import etree
from django.db import models
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django import template


#def index(request):
    #profiles = Profile.objects.all()
    #print(request)
    #return render(request, 'index.html', {'users': users})

def detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'detail.html', {'book': book})


class SearchResultsView(ListView):
    #model = User
    template_name = 'search.html'
    print("SearchResultsView")
    paginate_by = 20

    def get_queryset(self): 
        object_list = []
        title_list = []
        other_list = []
        query = self.request.GET
        title = query.get('title')
        print(title)
        authors = str(query.get('authors')).split(',')
        print(authors)
        isbn= query.get('isbn')
        print(isbn)
        book_url = query.get('book_url')
        print(book_url)
       
        search(book_title=title, authors=authors,isbn_13=isbn,url=book_url)
        #if query is None:
            #query = "abcdefhijklmnopqrstuvwxyz"
        #title_list = Book.objects.filter(Q(title__icontains=query))
        #other_list = Book.objects.filter(Q(authors__icontains=query) | Q(isbn_13__icontains=query) | Q(subtitle__icontains=query)
        #    | Q(series__icontains=query) | Q(volume__icontains=query) | Q(desc__icontains=query) | Q(book_formats__icontains=query)
        #    | Q(sale_flag__icontains=query))

        #for x in title_list:
        #    object_list.append(x)
        #for x in other_list:
        #    object_list.append(x)
        return object_list

def SearchForm(request):
	#creating a new form
	form = SignupForm()

	return render(request, 'search.html', {'form':form})


