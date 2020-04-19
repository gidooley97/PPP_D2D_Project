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
    Book_Url= forms.URLField(label='Book-url', max_length=100)



class EditForm(forms.Form):

    company_name = forms.CharField(max_length=50, label = "Company Name", widget=forms.TextInput(attrs={'class' : 'com_name'},))
    formats = MultiSelectFormField(label = "Formats", choices=MY_FORMATS,widget=forms.CheckboxSelectMultiple(attrs={'class':'frmts'}))
    search_these = MultiSelectFormField(label = "Searchable Sites", choices=SITES_TO_SEARCH, widget=forms.CheckboxSelectMultiple(attrs={'class':'sites'}))
    contact_fname = forms.CharField(widget = forms.HiddenInput(), required = False)
    contact_lname = forms.CharField(widget = forms.HiddenInput(), required = False)
    contact_email = forms.CharField(widget = forms.HiddenInput(), required = False)

class AddForm(forms.Form):

    company_name = forms.CharField(max_length=50, label = "Company Name", widget=forms.TextInput(attrs={'class' : 'com_name'},))
    formats = MultiSelectFormField(label = "Formats", choices=MY_FORMATS,widget=forms.CheckboxSelectMultiple(attrs={'class':'frmts'}))
    search_these = MultiSelectFormField(label = "Searchable Sites", choices=SITES_TO_SEARCH, widget=forms.CheckboxSelectMultiple(attrs={'class':'sites'}))
    username = forms.CharField(label="Username",widget=forms.TextInput(), required = True)
    contact_fname = forms.CharField(label="First Name",widget=forms.TextInput(), required = True)
    contact_lname = forms.CharField(label="Last Name",widget=forms.TextInput(), required = True)
    contact_email = forms.CharField(label="Email",widget=forms.TextInput(), required = True)


class FilterForm(forms.Form):
    TIME_RANGE_CHOICES=[("d", "Daily"),("w", "Weekly"),("m", "Monthly"),("y", "Yearly"),("a","All-time")]
	#start_date = forms.DateField()
    time_range = forms.ChoiceField(choices=TIME_RANGE_CHOICES, required=True)
	#end_date = forms.DateField()