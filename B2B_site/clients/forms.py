#importing forms
from django import forms 
from .models import *

#creating our forms
class SearchForm(forms.Form):
	#django gives a number of predefined fields
	#CharField and EmailField are only two of them
	#go through the official docs for more field details
	Title = forms.CharField(label='Title:', max_length=100)
	Author = forms.CharField(label='Author:', max_length=100)
	ISBN = forms.CharField(label='ISBN:', max_length=100)
	Book_Url= forms.URLField(label='Book-url', max_length=100)

class UpdateUserForm(forms.Form):

	first_name = forms.CharField(max_length=50, label = 'First Name')
	last_name = forms.CharField(max_length=50, label = 'Last Name')
	username = forms.CharField(max_length=50, label = 'Username')
	
