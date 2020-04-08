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
from .serializers import SiteBookDataSerializer
from rest_framework.response import Response 
from rest_framework.views import APIView 
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


def user_list(request):
    try:
        user = ""
    except User.DoesNotExist:
        raise Http404("User Does Not Exist")

    return render(request, 'user_list.html', {'user': user})

"""
This API calls the checkmate search module that uses the checkmate library to search for a given book.

Params:
    None
Return:
    JSON: serialized json of book matches.
"""
class SearchResultsView(APIView):
    
    print("SearchResultsView")
    
    def get(self,request): 
        book_matches = []#only a list of book matches no scores for now.
        print('request Meth:', request.method)
        query = self.request.GET
        title = query.get('title')
        print(title)
        authors = str(query.get('authors')).split(',')
        print(authors)
        isbn= query.get('isbn')
        print(isbn)
        book_url = query.get('book_url')
        print(book_url)
        if title is None:
            title="Lord" ##Change this value. if you want to search by a differnt book title.
        object_list=search(book_title=title, authors=authors,isbn_13=isbn,url=book_url)
        print(object_list)        
        serializer = SiteBookDataSerializer(object_list, many=True)
        return Response({"books":serializer.data})


def SearchForm(request):
	#creating a new form
	form = SignupForm()

	return render(request, 'search.html', {'form':form})

class logoutView(TemplateView):
    template_name = 'registration/logged_out.html'

class loginView(TemplateView):
    template_name = 'registration/login.html'

