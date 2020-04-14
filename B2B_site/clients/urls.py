from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from . import views


urlpatterns = [
    path('search/', views.SearchView, name='search'),
    path('', views.SearchView, name='search'),
    path('api/search/', views.SearchAPIView.as_view(), name='search_api'),#This is an API
    path('companies/', views.list_companies, name='companies'),
    # path('logout/', views.LogoutView.as_view(), name='logged_out'),
    # path('login/', views.LoginView.as_view(), name='login'), #No need for these
    path('activity/', views.activity, name='activity'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), #to get the auth token send a POST request http://127.0.0.1:8000/clients/api-token-auth/ with the body{ username:<username>, password:<pass>}
    
]
