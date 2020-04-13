#importing forms
from django import forms 

#creating our forms
class SearchForm(forms.Form):
	#django gives a number of predefined fields
	#CharField and EmailField are only two of them
	#go through the official docs for more field details
	Title = forms.CharField(label='Title:', max_length=100)
	Author = forms.CharField(label='Author:', max_length=100)
	ISBN = forms.CharField(label='ISBN:', max_length=100)
    #Book_Url= forms.URLField(label='Book-url', max_lenght=100)

class JsonSearchForm(forms.Form):
	Json_data = forms.Textarea(label='Json', cols='76', rows='15')

