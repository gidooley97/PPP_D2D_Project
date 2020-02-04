from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('simple_upload', views.simple_upload, name='simple_upload'),
    path('onixfile', views.onixfile, name='onixfile'),
]