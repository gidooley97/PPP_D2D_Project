#importing forms
from django import forms 
from multiselectfield import MultiSelectFormField
from .models import *
from .models import MY_FORMATS
from .models import SITES_TO_SEARCH


class TextForm(forms.Form):
	title = forms.CharField(label = 'Title:', max_length=100)
	authors = forms.CharField(label='Authors:', max_length=100)
	isbn = forms.CharField(label='ISBN:', max_length=100)

	def is_valid(self):
		valid = super(TextForm, self).is_valid()

		if not valid:
			return valid

		if (self.cleaned_data['title'] is "" and self.cleaned_data['authors'] is "" and
			 self.cleaned_data['isbn'] is ""):
			raise forms.ValidationError(
				"Must populate atleast one field if not searching with JSON")
		
		if sum(self.cleaned_data['isbn'].isdigit() for c in self.cleaned_data['isbn']) != 13:
			raise forms.ValidationError("ISBN must contain 13 digits.")



class JsonForm(forms.Form):
    json = forms.Textarea

    def clean_jsonfield(self):
         jdata = self.cleaned_data['jsonfield']
         try:
             json_data = json.loads(jdata) #loads string as json
             #validate json_data
         except:
             raise forms.ValidationError("Invalid data in jsonfield")
         #if json data not valid:
            #raise forms.ValidationError("Invalid data in jsonfield")
         return jdata



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