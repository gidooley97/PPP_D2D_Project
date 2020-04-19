from django.shortcuts import render

from django.views import generic, View
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .search_checkmate import search
from lxml import etree
from django.db import models
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django import template
from .models import Profile, Query_Manager
from django.contrib.auth.models import Group
from .serializers import SiteBookDataSerializer
from rest_framework.response import Response 
from rest_framework.views import APIView 
from .forms import UpdateUserForm, AddUserForm

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


def list_companies(request):
    group_list = Group.objects.all()
    return render(request, "company_list.html", {"group_list": group_list})

#def company_report(request):
 #   return render(request, "company_report.html")

class logoutView(TemplateView):
    template_name = 'registration/logged_out.html'

class loginView(TemplateView):
    template_name = 'registration/login.html'

def admin_users_list(request):
    user_list = User.objects.all()
    return render(request, "user_list.html", {"user_list": user_list})

def user_edit_form(request,user_id):
    user = User.objects.get(id = user_id)

    form = UpdateUserForm(initial = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'username': user.username, 'password': user.password, 'is_staff': user.is_staff})

    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password']
            user.save()
            return HttpResponseRedirect(reverse('users'))

    else:
        form = UpdateUserForm(initial = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 
        'username': user.username, 'password': user.password, 'is_staff': user.is_staff})
    return render(request, "update_user.html", {'form': form, 'first_name': user.first_name, 'last_name': user.last_name, 
    'email': user.email, 'username': user.username, 'password': user.password, 'is_staff': user.is_staff})

def user_add_form(request):
    form = AddUserForm(request.POST)

    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            User.objects.create(first_name=first_name)
            user = User.objects.get(first_name=first_name)
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password']

            user.save()
            return HttpResponseRedirect(reverse('users'))

    else:
        form = AddUserForm(request.POST)
    return render(request, "add_user.html", {'form': form})


def list_users(request):                    #This is the Report Page
    group_list = Group.objects.all()
    user_list = User.objects.all()
    return render(request, "activity.html", {"group_list": group_list, "user_list": user_list}) #connection with database


