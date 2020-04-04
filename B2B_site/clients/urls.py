from django.urls import path

from . import views

urlpatterns = [
    path('', views.SearchResultsView.as_view(), name='search'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
]
