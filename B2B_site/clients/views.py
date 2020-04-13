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
from .forms import EditForm

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
This search api requires authentication
Params:
    None
Return:
    JSON: serialized json of book matches.
"""
#GET /clients/api/search?params and headers Authorizatio:<>
#TO generate auth token:run python3 manage.py drf_create_token <username>
class SearchAPIView(APIView):
    permission_classes = (IsAuthenticated,) #requires authentication
    def get(self,request): 
        book_matches = []#only a list of book matches no scores for now.
        try:
            user = request.user
            company = Group.objects.filter(user=request.user)[0]
            permissions = company.permissions.all()#getting company's permissions
            perm_codenames = list(map(lambda x:x.codename,permissions))
            query = self.request.GET
            
            book_matches = process(perm_codenames,query)
            print( book_matches)        
            serializer = SiteBookDataSerializer( book_matches, many=True)
        except:
            content ={"Error":"Something went wrong. Make sure you have access to this API."}
            return Response(content, status=status.HTTP_404_NOT_FOUND) 

        #Tracking system
        p = Profile.objects.get(user=user)
        try:
            q_m  = Query_Manager.objects.get(user=p,last_date__exact=datetime.date.today())
            q_m.num_queries +=1
            q_m.save() 
                
        except Query_Manager.DoesNotExist:
            print("Creating new query manager with new date") 
            new_q_m= Query_Manager.objects.create(user=p, num_queries=1, last_date=datetime.date.today(),)
        
        return Response({"books":serializer.data}, status.HTTP_200_OK)



@login_required(login_url='/accounts/login/')
def SearchView(request):

	return render(request, 'search.html')


@login_required(login_url='/accounts/login/')
def list_companies(request):
    group_list = Group.objects.all()
    return render(request, "company_list.html", {"group_list": group_list})

#def company_report(request): #no one will ever access these views
# We will ourselves ask therm to login and give them an option to logout 
 #   return render(request, "company_report.html")

# class LogoutView(TemplateView):
#     template_name = 'registration/logged_out.html'

# class LoginView(TemplateView):
#     template_name = 'registration/login.html'

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


@login_required(login_url='/accounts/login/')
def activity(request):                    #This is the Report Page
    # group_list = Group.objects.all() #no need to get all groups
    user = request.user 
    #let's do something different for admin users
    group = user.groups.all()[0]
    if user == 'admin':
        #do something
        pass
    p = Profile.objects.get(user=user)
    q_m= Query_Manager.objects.filter(user=p)
    perm = group.permissions.all()
    print('group',perm[0].name)
    users_in_group = User.objects.filter(groups__name=group)
    #Take care of getting queries made
    return render(request, "activity.html", {"group": group, "user_list":users_in_group}) #connection with database


def company_edit_form(request,group_id):
    group = Group.objects.get(id = group_id)
    permissions = group.permissions.all()

    #------ Get Company Contact ----------
    contact = group.contact_user
  
    form = EditForm(initial = { 'company_name': group.name, 'search_these' : permissions, 'formats': group.format})

    if request.method == 'POST':
        form = EditForm(request.POST) # if post method then form will be validated
        if form.is_valid():
            clean_name = form.cleaned_data['company_name']
            group.name = clean_name
            clean_permissions = form.cleaned_data['search_these']
            #group.permissions.set(clean_permissions) #Let's use a multiselect for the websites in the Group model
            clean_format =  form.cleaned_data['formats']
            group.format = clean_format
            group.save()
            return HttpResponseRedirect(reverse('companies') )

    else:
        form = EditForm(initial = {'company_name': group.name, 'search_these' : permissions})
    return render(request, "company_edit.html",{'form': form, 'contact_fname' : contact.first_name,
     'contact_lname': contact.last_name, 'contact_email': contact.email})
