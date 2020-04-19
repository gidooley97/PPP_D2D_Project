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
	first_name = forms.CharField(label="First Name", widget=forms.TextInput(), required = True)
	last_name = forms.CharField(label="Last Name", widget=forms.TextInput(), required = True)
	email = forms.CharField(label="Email Address", widget=forms.TextInput(), required = True)
	username = forms.CharField(label="Username", widget=forms.TextInput(), required = True)
	password = forms.CharField(label="Password", widget=forms.PasswordInput(), required = True)
	is_staff = forms.BooleanField(label = "Is Staff?", required = False)

class AddUserForm(forms.Form):
	first_name = forms.CharField(label="First Name", widget=forms.TextInput(), required = True)
	last_name = forms.CharField(label="Last Name", widget=forms.TextInput(), required = True)
	email = forms.CharField(label="Email Address", widget=forms.TextInput(), required = True)
	username = forms.CharField(label="Username", widget=forms.TextInput(), required = True)
	password = forms.CharField(label="Password", widget=forms.PasswordInput(), required = True)
	is_staff = forms.BooleanField(label = "Is Staff?", required = False)