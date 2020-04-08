from django.urls import path

from . import views

urlpatterns = [
    path('', views.SearchView.as_view(), name='search'),
    path('search/api/', views.SearchResultsView.as_view(), name='search_api'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('logout/', views.logoutView.as_view(), name='logged_out'),
    path('login/', views.loginView.as_view(), name='login'),


]
