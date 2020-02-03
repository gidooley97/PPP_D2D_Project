from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('simple_upload', views.simple_upload, name='simple_upload'),
]