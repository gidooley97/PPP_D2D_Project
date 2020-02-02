from __future__ import unicode_literals
from django.db import models


class Book(models.Model):
    FORMAT_TYPES = (
        ('H', 'Hardcover'),
        ('P', 'Paperback'),
        ('E', 'Ebook'),
        ('A', 'Audio')
    )
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    isbn_13 = models.CharField(max_length = 13)
    subtitle = models.CharField(max_length=200, default = '', blank=True)
    series = models.CharField(max_length = 200,default = '', blank=True)
    volume = models.CharField(max_length = 3, default = '', blank=True)
    desc = models.TextField()
    book_format = models.CharField(max_length=1, choices=FORMAT_TYPES)
    sale_flag = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title
   

class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
