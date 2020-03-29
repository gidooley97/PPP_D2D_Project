from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length=70,unique=True)
    num_queries = models.IntegerField() 

    def __str__(self):              
        return self.first_name + self.last_name
    
    def get_email(self):
        return self.email
    
    