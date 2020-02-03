from django import forms

from . import models
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)
