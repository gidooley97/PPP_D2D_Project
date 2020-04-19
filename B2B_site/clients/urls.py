from django.urls import path

from . import views

urlpatterns = [
    path('', views.SearchResultsView.as_view(), name='search'),
    path('search/', views.SearchResultsView.as_view(), name='search'),#This is an API
    
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('companies/', views.list_companies, name='companies'),
    path('users/', views.admin_users_list, name='users'),
    path('users/update/<int:user_id>', views.user_edit_form, name='user_edit_form'),
    path('users/add/', views.user_add_form, name='user_add_form'),
    path('logout/', views.logoutView.as_view(), name='logged_out'),
    path('login/', views.loginView.as_view(), name='login'),
    path('activity/', views.list_users, name='activity'),
    
]
