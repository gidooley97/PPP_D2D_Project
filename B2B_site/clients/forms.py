#importing forms
from django import forms 

#creating our forms
class SearchForm(forms.Form):
	#django gives a number of predefined fields
	#CharField and EmailField are only two of them
	#go through the official docs for more field detail
    Title = forms.CharField(label='Title:', max_length=100)
    Author = forms.CharField(label='Author:', max_length=100)
    ISBN = forms.CharField(label='ISBN:', max_length=100)
    Book_Url= forms.URLField(label='Book-url', max_length=100)
	

class EditForm(forms.Form):
    
    SEARCH_CHOICES = (
        ('Kobo', 'Kobo'),
        ('Livraria_Cultura', 'Livraria_Cultura'),
        ("Test_Book_Store", 'Test_Book_Store'),
        ("Scribd", "Scribd"),
        ("Audio_Books", "Audio_Books"),
        ("Google_Books", "Google_Books")
    )

    company_name = forms.CharField(max_length=50, label = "Company Name", widget=forms.TextInput(attrs={'class' : 'x'}))
    search_these = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SEARCH_CHOICES)
    contact_fname = forms.CharField(widget = forms.HiddenInput(), required = False)
    contact_fname = forms.CharField(widget = forms.HiddenInput(), required = False)
    contact_email = forms.CharField(widget = forms.HiddenInput(), required = False)
