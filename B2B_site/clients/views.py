from django.shortcuts import render
import requests
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
from django.contrib.auth.models import Group, Permission
from .search_checkmate import process
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
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from rest_framework.permissions import IsAuthenticated
from .forms import EditForm, AddForm, FilterForm, TextForm, JsonForm, UpdateUserForm, AddUserForm, DeleteUserForm, DeleteForm
from datetime import date
from .filter_dates import filter_dates, get_time_range
import json


"""
This API calls the checkmate search module that uses the checkmate library to search for a given book.
This search api requires authentication
Params:
    None
Return:
    JSON: serialized json of book matches.
"""
# GET /clients/api/search?params and headers Authorizatio:<>
# TO generate auth token:run python3 manage.py drf_create_token <username>
class SearchAPIView(APIView):
    permission_classes = (IsAuthenticated,)  # requires authentication

    def get(self, request,):
        return request_processor(request)
    def post(self, request, format=None):
        return request_processor(request)        

"""
processes the request by calling the checkmate library.

params:
    request: if get request, parameters are query, if post it is json
returns:
    json response: json containing matches
"""
def request_processor(request):
    book_matches = []  # only a list of book matches no scores for now.
    try:
        user = request.user
        company = Group.objects.filter(user=request.user)[0]
        sites_allowed = list(company.search_sites)
        formats = list(company.formats)
        if not sites_allowed or not formats:
            content = {
                "Error": "User does not have access to any sites or formats."
                }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        query = request.GET
        data =None

        if request.method=="POST":
            data = request.data
    
        if data:  # we can only use json or the other attributs
            query = None
        book_matches = process(sites_allowed, formats, query, data)
        if book_matches is None:
            raise Exception
        print(book_matches)
        serializer = SiteBookDataSerializer(book_matches, many=True)
    except Exception as e:
        print(e)
        content = {
            "Error": "Something went wrong. Make sure you have access to this API."}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    p = Profile.objects.get(user=user)
    addQuery(p)
        
    return Response({"books":serializer.data}, status.HTTP_200_OK)    

"""
displays search page and handles get and post requests for searches
interfaces with checkmate library through search_checkmate
accesses user to ensure they only access their sites and their queries are counted

params:
    request: get or post request holding fields to be queried
returns:
    context: dict containing list of books resulting from checkmate search
"""
@login_required(login_url='/accounts/login/')
def search(request):
    context = {}

    if (request.GET or request.POST): 
        try:
            user = request.user
            company = user.groups.all()[0]
            sites_allowed = list(company.search_sites)
            formats = list(company.formats)
            query = ""
            data = "" 
            
            if request.method == "GET":
                query = request.GET
            if request.method == "POST":
                data = json.loads(request.POST['json'])

            book_matches = process(sites_allowed,formats,query,data)
            print( book_matches)        
            book_dict = SiteBookDataSerializer( book_matches, many=True)
            context = {"books":book_dict.data}
            

        except Exception as e:
            print(e)
            content ={"Error":"Something went wrong. Make sure you have access to this API."}
            return render(request, 'search.html', content) 

        p = Profile.objects.get(user=user)
        if book_matches:
            addQuery(p)
        
    return render(request, 'search.html', context)
    

"""
handles incrementing number of searches made by a user
if no query manager exists for the user on this date, create new one
params:
    user: the user making the query on the checkmate tool
returns:
    none
"""
def addQuery(user):
    try:
        q_m  = Query_Manager.objects.get(user=user,last_date__exact=datetime.date.today())
        q_m.num_queries +=1
        q_m.save() 
                
    except Query_Manager.DoesNotExist:
        new_q_m= Query_Manager.objects.create(user=user, num_queries=1, last_date=datetime.date.today(),)


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

"""
List out all the users in B2B database
params:
    request: the request for the list view
returns:
    User list view
"""
@login_required(login_url='/accounts/login/')
def admin_users_list(request):
    user_list = User.objects.all()
    return render(request, "user_list.html", {"user_list": user_list})

"""
Gets the edit form from forms.py and displays the edit view
params:
    request: the request for the edit view
    user_id: the id of the user so the exact person can be aquired 
returns:
    If success, return the user list view
    If fail, return update view to original state
"""
@login_required(login_url='/accounts/login/')
def user_edit_form(request,user_id):
    user = User.objects.get(id = user_id)

    form = UpdateUserForm(initial = { 'company': Group.objects.get(user=user), 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'username': user.username, 
        'password': user.password, 'is_staff': user.is_staff})

    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.is_staff = form.cleaned_data['is_staff']
            group = Group.objects.get(name=form.cleaned_data['company'])
            user.groups.clear()
            user.groups.add(group)

            user.save()
            group.save()
            return HttpResponseRedirect(reverse('users'))

    else:
        form = UpdateUserForm(initial = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 
        'username': user.username, 'password': user.password, 'is_staff': user.is_staff, 'company': Group.objects.get(user=user)})
    return render(request, "update_user.html", {'form': form, 'first_name': user.first_name, 'last_name': user.last_name, 
    'email': user.email, 'username': user.username, 'password': user.password, 'is_staff': user.is_staff, 'company': Group.objects.filter(user=request.user)})

"""
Get the add user form in forms.py and displays the add user view
params:
    request: the request for the add view
returns:
    If success, return list view
    If fail, return the empty form
"""
@login_required(login_url='/accounts/login/')
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
            user.is_staff = form.cleaned_data['is_staff']
            group = Group.objects.get(name=form.cleaned_data['company'])
            group.user_set.add(user)

            group.save
            user.save()
            return HttpResponseRedirect(reverse('users'))

    else:
        form = AddUserForm(request.POST)
    return render(request, "add_user.html", {'form': form})

"""
Get the add user form in forms.py and displays the add user view
params:
    request: the request for the add view
returns:
    If success, return list view
    If fail, return the empty form
"""
@login_required(login_url='/accounts/login/')
def user_delete_form(request, user_id):
    user = User.objects.get(id = user_id)

    form = DeleteUserForm(request.POST)

    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            User.objects.get(id = user_id).delete()

            return HttpResponseRedirect(reverse('users'))

    else:
        form = DeleteUserForm(request.POST)
    return render(request, "delete_user.html", {'form': form, 'first_name': user.first_name, 'last_name': user.last_name})


def list_users(request):                    #This is the Report Page
    group_list = Group.objects.all()
    user_list = User.objects.all()
    return render(request, "activity.html", {"group_list": group_list, "user_list": user_list}) #connection with database

@login_required(login_url='/accounts/login/')
def activity(request):                    #This is the Report Page
    user = request.user 
    groups = None
    if user.is_staff:
        groups = Group.objects.all()
    elif user.groups.all():
        groups = user.groups.all()

    companies_report = filter_dates(groups, "d")
    time_range= get_time_range('d')
    form = FilterForm()
    if request.method == 'POST':
        form = FilterForm(request.POST) # if post method then form will be validated      try with: 2020-4-10 to 2020-4-12 : output should be 19
        if form.is_valid():
            companies_report = filter_dates(groups, form.cleaned_data['time_range'])
            time_range= get_time_range(form.cleaned_data['time_range'])
            time_range = "showing results for "+time_range
            return render(request, "activity.html", {"form":form, "companies_report":companies_report,"time_range":time_range})
    else:
        form = FilterForm()
    time_range = "showing results for "+time_range
    return render(request, "activity.html", {"form":form,"companies_report":companies_report, "time_range":time_range }) 

@login_required(login_url='/accounts/login/')
def list_companies(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('search') )
    group_list = Group.objects.all()
    return render(request, "company_list.html", {"group_list": group_list})

#view to edit the company, login required, staff members only have access
@login_required(login_url='/accounts/login/')
def company_edit_form(request,group_id):
    group = Group.objects.get(id = group_id) #getting our company by group_id
    contact = group.contact_user #getting our company contact_user
    
    form = EditForm(initial = {'company_name': group.name, 'search_these' : group.search_sites, 'formats': group.formats})

    if request.method == 'POST':
        form = EditForm(request.POST) 
        if form.is_valid():
            clean_name = form.cleaned_data['company_name']
            group.name = clean_name
            clean_format =  form.cleaned_data['formats']
            group.formats = clean_format
            clean_sites = form.cleaned_data['search_these']
            group.search_sites = clean_sites
            group.save()
            return HttpResponseRedirect(reverse('companies') )

    else:
        form = EditForm(initial = {'company_name': group.name, 'search_these' : group.search_sites, 'formats': group.formats})
    return render(request, "company_edit.html",{'form': form, 'contact_fname' : contact.first_name,
     'contact_lname': contact.last_name, 'contact_email': contact.email})

#view to add a company, login required, staff members only have access
@login_required(login_url='/accounts/login/')
def company_add_form(request):

    form = AddForm(request.POST)

    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            #company creation
            clean_name = form.cleaned_data['company_name']
            Group.objects.create(name=clean_name) #creates group based on what is in the company_name field
            group = Group.objects.get(name=clean_name)
            clean_format =  form.cleaned_data['formats']
            group.formats = clean_format
            clean_sites = form.cleaned_data['search_these']
            group.search_sites = clean_sites
            #contact_user creation
            clean_username = form.cleaned_data['username']
            User.objects.create(username=clean_username) #creates user object based on what is in the username field
            user = User.objects.get(username=clean_username)  
            clean_fname = form.cleaned_data['contact_fname']
            user.first_name = clean_fname
            clean_lname = form.cleaned_data['contact_lname']
            user.last_name = clean_lname
            clean_email = form.cleaned_data['contact_email']
            user.email = clean_email
            user.save() 
            group.contact_user = user #assigns our created as contact_user in company
            group.save()
            return HttpResponseRedirect(reverse('companies'))

    else:
        form = AddForm(request.POST)
    return render(request, "company_add.html", {'form': form})

#view to delete a company, login required, staff members only have access
@login_required(login_url='/accounts/login/')
def company_delete_form(request, group_id):
    group = Group.objects.get(id = group_id)

    form = DeleteForm(request.POST)

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():  
            Group.objects.get(id = group_id).delete() #gets company to delete by group_id
            return HttpResponseRedirect(reverse('companies'))

    else:
        form = DeleteForm(request.POST)
    return render(request, "company_delete.html", {'form': form,'company_name': group.name})
