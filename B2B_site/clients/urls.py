from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('', views.SearchResultsView.as_view(), name='search'),
    path('search/', views.SearchResultsView.as_view(), name='search'),#This is an API
    
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('companies/', views.list_companies, name='companies'),
    path('logout/', views.logoutView.as_view(), name='logged_out'),
    path('login/', views.loginView.as_view(), name='login'),
    path('activity/', views.list_users, name='activity'),
    
]
