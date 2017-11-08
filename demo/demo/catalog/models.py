from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



# Create your models here.


#this model extends the Django default user model. It can be used to give attributes to users
#like we need in our project specifications
    #example use: in views.py if you want to deal with a company user -
        #if request.user.profile.is_company:
            #whatever code here
class profile(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    is_manager = models.BooleanField(default = False)
    objects = models.Manager()

    #the signup view will set this to True if the radio button Investor is chosen
    is_company = models.BooleanField(default = False)

    #if user's is_manager field is True, they can set another user's is_suspended to True
    is_suspended = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Report(models.Model):
    company = models.CharField(max_length=30, help_text="Company name")

    phone = models.CharField(max_length=20, help_text="Company phone number")

    location = models.CharField(max_length=20, help_text="Company location")

    country = models.CharField(max_length=30, help_text="Company country")

    sector = models.CharField(max_length=30, help_text="Company sector")

    industry = models.CharField(max_length=30, help_text="Company industry")

    created_by = models.ForeignKey(User)

    objects = models.Manager()








