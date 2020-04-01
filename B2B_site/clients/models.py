from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    query_data = models.CharField(max_length = 17)

    def get_num_queries_month(q_string,month):
        query_values = q_string

        return num_queries
    
    def get_num_queries_year(q_string, year):


    def get_num_queries_ever(q_string):



    def inc_num_queries():
        num_queries += 1

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()