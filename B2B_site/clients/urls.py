from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.SearchView, name='search'),
    path('', views.SearchView, name='search'),
    path('api/search/', views.SearchAPIView.as_view(), name='search_api'),#This is an API
    path('companies/', views.list_companies, name='companies'),
    # path('logout/', views.LogoutView.as_view(), name='logged_out'),
    # path('login/', views.LoginView.as_view(), name='login'), #No need for these
    path('activity/', views.activity, name='activity'),
    
]
