from django.shortcuts import render
from . import views
from django.views import generic, View


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    print(request)
    return render(request, 'index.html')
