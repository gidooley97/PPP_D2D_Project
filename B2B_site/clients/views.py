from django.shortcuts import render
import requests
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
from django.contrib.auth.decorators import login_required
import datetime
from rest_framework.permissions import IsAuthenticated
from .forms import EditForm, FilterForm
from datetime import date
from .filter_dates import filter_dates


# def index(request):
    # profiles = Profile.objects.all()
    # print(request)
    # return render(request, 'index.html', {'users': users})

# def detail(request, book_id):
#     try:
#         book = Book.objects.get(pk=book_id)
#     except Book.DoesNotExist:
#         raise Http404("Question does not exist")

#     return render(request, 'detail.html', {'book': book})

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
    request:
returns:
    json response: json contsining matches
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
    # Tracking system
    p = Profile.objects.get(user=user)
    try:
        q_m = Query_Manager.objects.get(
        user=p, last_date__exact=datetime.date.today())
        q_m.num_queries += 1
        q_m.save()

    except Query_Manager.DoesNotExist:
        print("Creating new query manager with new date") 
        new_q_m= Query_Manager.objects.create(user=p, num_queries=1, last_date=datetime.date.today(),)
        
    return Response({"books":serializer.data}, status.HTTP_200_OK)    


@login_required(login_url='/accounts/login/')
def SearchView(request):
    # text_form = SearchForm()
    # json_form = JsonSearchForm()
    return render(request, 'search.html')


@login_required(login_url='/accounts/login/')
def list_companies(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('search') )
    group_list = Group.objects.all()
    return render(request, "company_list.html", {"group_list": group_list})


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


@login_required(login_url='/accounts/login/')
def activity(request):                    #This is the Report Page
    # group_list = Group.objects.all() #no need to get all groups
    user = request.user 
    if not user.groups.all():
        raise Http404("User does not belong to any group")
    group = user.groups.all()[0]
    if user == 'admin':
        # do something
        pass
    p = Profile.objects.get(user=user)
    q_m= Query_Manager.objects.filter(user=p) #, last_date__range=(date(2020,1,1), date(2020, 2, 9)))[0]
    perm = group.permissions.all()
    print('group',perm[0].name)
    users_in_group = User.objects.filter(groups__name=group)
    # Take care of getting queries made
   
    form = FilterForm()
    if request.method == 'POST':
        form = FilterForm(request.POST) # if post method then form will be validated      try with: 2020-4-10 to 2020-4-12 : output should be 19
        if form.is_valid():
            company_report = filter_dates(group, form.cleaned_data['time_range'])
            #print("time range", form.cleaned_data['time_range'])
            #q_m = Query_Manager.objects.filter(user=p, last_date__range=(form.cleaned_data['start_date'], form.cleaned_data['end_date']))[0]
            #q_m.save()
            #return HttpResponseRedirect(reverse(request, "activity", {"group": group, "user_list":users_in_group, "q_m":q_m, "form":form}))
            return render(request, "activity.html", {"form":form, "group": group,"company_report":company_report})
    else:
        form = FilterForm()
    #return render(request, "activity.html", {"group": group, "user_list":users_in_group, "q_m":q_m, "form":form}) #connection with database
    return render(request, "activity.html", {"form":form,"group": group }) #connection with database


@login_required(login_url='/accounts/login/')
def company_edit_form(request,group_id):
    group = Group.objects.get(id = group_id)
    contact = group.contact_user
    # ------ Get Company Contact ----------
    
    form = EditForm(initial = {'company_name': group.name, 'search_these' : group.search_sites, 'formats': group.formats})

    if request.method == 'POST':
        form = EditForm(request.POST) # if post method then form will be validated
        if form.is_valid():
            clean_name = form.cleaned_data['company_name']
            group.name = clean_name
            clean_permissions = form.cleaned_data['search_these']
            # group.permissions.set(clean_permissions) #Let's use a multiselect for the websites in the Group model
            clean_format =  form.cleaned_data['formats']
            group.format = clean_format
            clean_sites = form.cleaned_data['search_these']
            group.search_sites = clean_sites
            group.save()
            return HttpResponseRedirect(reverse('companies') )

    else:
        form = EditForm(initial = {'company_name': group.name, 'search_these' : group.search_sites, 'formats': group.formats})
    return render(request, "company_edit.html",{'form': form, 'contact_fname' : contact.first_name,
     'contact_lname': contact.last_name, 'contact_email': contact.email})

@login_required(login_url='/accounts/login/')
def company_add_form(request):
    # ------ Get Company Contact ----------

    form = EditForm(request.POST)

    if request.method == 'POST':
        form = EditForm(request.POST) # if post method then form will be validated
        if form.is_valid():
            
            clean_name = form.cleaned_data['company_name']
            Group.objects.create(name=clean_name)
            group = Group.objects.get(name=clean_name)
            clean_permissions = form.cleaned_data['search_these']
            # group.permissions.set(clean_permissions) #Let's use a multiselect for the websites in the Group model
            clean_format =  form.cleaned_data['formats']
            group.format = clean_format
            clean_sites = form.cleaned_data['search_these']
            group.search_sites = clean_sites
            group.save()
            return HttpResponseRedirect(reverse('companies'))

    else:
        form = EditForm(request.POST)
    return render(request, "company_add.html", {'form': form})
