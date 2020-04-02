from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def query_handler(self, date):        
        q_set =  Query_Manager.objects.all()
        for q in q_set:
            if date.date == q.get_date().date:
                q.inc_num_queries
            else:
                new_qm = Query_Manager(last_date = date)
                new_qm.inc_num_queries


class Query_Manager(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    num_queries = models.IntegerField(default =0)
    last_date = models.DateField()

    def get_num_queries():
        return num_queries
    
    def inc_num_queries():
        num_queries += 1
    
    def get_date():
        return last_date

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()