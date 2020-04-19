from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType 
import datetime


from multiselectfield import MultiSelectField

MY_FORMATS = (
    ('ebook', "Ebook"),
    ('audio', "Audio Book"),
    ('hard_cover', 'Hard Cover'),
    ('paper_back', 'Paper Back')
)

SITES_TO_SEARCH =(
    ('kobo', "Kobo"),
    ('google_books',"Google Books"),
    ('scribd', "Scribd"),
    ('audio_books', "Audio Books"),
    ('test_store', "Test Book Store"),
    ('livraria cultura', "Livraria Cultura")
)
Group.add_to_class('formats',MultiSelectField(choices=MY_FORMATS, max_length=50, blank = True))
Group.add_to_class('search_sites',MultiSelectField(choices=SITES_TO_SEARCH, max_length=80, blank = True))
Group.add_to_class('contact_user', models.OneToOneField(User, on_delete=models.CASCADE,  null = True))

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def query_handler(self, date):  
        try:#user made queries on this date
            q_set = Query_Manager.objects.get(last_date = date)
            q_set.inc_num_queries
        except:
            new_qm = Query_Manager(user=self.user,num_queries=1,last_date = date)
        finally:
            new_qm.save()
    def __str__(self):
        return self.user.first_name+','+self.user.last_name
        

class Query_Manager(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    num_queries = models.IntegerField(default =0)
    last_date = models.DateField(default= datetime.date.today)

    def get_num_queries(self):
        return self.num_queries
    
    def inc_num_queries(self):
        self.num_queries += 1
    
    def get_date(self):
        return self.last_date
    def __str__(self):
        return str(self.num_queries)+", "+str(self.last_date)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


    
