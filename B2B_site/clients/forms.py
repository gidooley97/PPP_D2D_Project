#importing forms
from django import forms 
from multiselectfield import MultiSelectFormField
from .models import *
from .models import MY_FORMATS
from .models import SITES_TO_SEARCH

#creating our forms
class SearchForm(forms.Form):
	#django gives a number of predefined fields
	#CharField and EmailField are only two of them

	#go through the official docs for more field details
	Title = forms.CharField(label='Title:', max_length=100)
	Author = forms.CharField(label='Author:', max_length=100)
	ISBN = forms.CharField(label='ISBN:', max_length=100)
    #Book_Url= forms.URLField(label='Book-url', max_lenght=100)

# class JsonSearchForm(forms.Form):
# 	Json_data = forms.Textarea(label='Json', cols='76', rows='15')


class EditForm(forms.Form):
    
    SEARCH_CHOICES = (
        ('Kobo', 'Kobo'),
        ('Livraria_Cultura', 'Livraria Cultura'),
        ("Test_Book_Store", 'Test Book Store'),
        ("Scribd", "Scribd"),
        ("Audio_Books", "Audio Books"),
        ("Google_Books", "Google Books")
    )

    # MY_FORMATS = (
    #     ('ebook', "Ebook"),
    #     ('audio', "Audio Book"),
    #     ('hard_cover', 'Hard Cover'),
    #     ('paper_back', 'Paper Back')
    # )

    company_name = forms.CharField(max_length=50, label = "Company Name", widget=forms.TextInput(attrs={'class' : 'com_name'},))
   # search_these = forms.MultipleChoiceField(label ="Searchable Sites",widget=forms.CheckboxSelectMultiple(attrs={'class':'perm'}), choices=SEARCH_CHOICES)
    #formats = forms.MultipleChoiceField(label ="Formats",widget=forms.CheckboxSelectMultiple(attrs={'class':'format'}), choices = FORMATS)
    formats = MultiSelectFormField(label = "Formats", choices=MY_FORMATS,widget=forms.CheckboxSelectMultiple(attrs={'class':'frmts'}))
    search_these = MultiSelectFormField(label = "Searchable Sites", choices=SITES_TO_SEARCH, widget=forms.CheckboxSelectMultiple(attrs={'class':'sites'}))
    contact_fname = forms.CharField(widget = forms.HiddenInput(), required = False)
    contact_fname = forms.CharField(widget = forms.HiddenInput(), required = False)
    contact_email = forms.CharField(widget = forms.HiddenInput(), required = False)




   # formats = MultiSelectFormField(choices=MyModel.MY_CHOICES)

class FilterForm(forms.Form):
	start_date = forms.DateTime(label='Start Date')
	end_date = forms.DateTime(label='End Date')