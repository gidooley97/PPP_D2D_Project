from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm


FORMAT_TYPES = (
        ('H', 'Hardcover'),
        ('P', 'Paperback'),
        ('E', 'Ebook'),
        ('A', 'Audio')
    )

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    isbn_13 = models.CharField(max_length = 13)
    subtitle = models.CharField(max_length=200, default = '', blank=True)
    series = models.CharField(max_length = 200,default = '', blank=True)
    volume = models.CharField(max_length = 3, default = '', blank=True)
    desc = models.TextField()
    book_formats = models.CharField(max_length=4)
    sale_flag = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title
    def formats_as_list(self):
        return list(self.book_formats)
   

class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

