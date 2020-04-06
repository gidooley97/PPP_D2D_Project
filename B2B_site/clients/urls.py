from django.urls import path

from . import views

urlpatterns = [
    path('', views.SearchResultsView.as_view(), name='search'),
    path('search/', views.SearchResultsView.as_view(), name='search'),#This is an API
    
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('logout/', views.logoutView.as_view(), name='logged_out'),
    path('login/', views.loginView.as_view(), name='login'),


]
