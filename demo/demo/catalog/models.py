from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group
# from django.utils import timezone
# import datetime
# from Crypto.PublicKey import RSA


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
    is_investor=models.BooleanField(default=False)
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
    report_no = models.AutoField(primary_key=True)

    #init_date = models.DateTimeField(default=timezone.now)

    current_projects = models.CharField(default= "No current Projects",max_length= 1000, help_text="Projects")

    company = models.CharField(max_length=30, help_text="Company name")

    funding_goal = models.CharField(max_length=20, help_text="Funding goal", default="10,000")

    phone = models.CharField(max_length=20, help_text="Company phone number")

    location = models.CharField(max_length=20, help_text="Company location")

    country = models.CharField(max_length=30,help_text="Company country")

    sector = models.CharField(max_length=30, help_text="Company sector")

    industry = models.CharField(max_length=30, help_text="Company industry")

    description=models.CharField(default="No description yet",max_length=3000,help_text="Project description")

    #created_by = models.ForeignKey(User)

    #objects = models.Manager()

    #have to be able to mark reports as private
    is_private = models.BooleanField(default = False)

class Message(models.Model):
    receiver = models.CharField(max_length= 30, help_text="Receiver",default="")

    sender = models.CharField(max_length=30, help_text="Sender",default="")

    message = models.CharField(max_length= 5000, help_text='message',default="")

    encrypt=models.BooleanField(default=False)



class KeyPair(models.Model):
    user = models.OneToOneField(User)
    RSAkey = models.CharField(max_length=15000)
    pubkey=models.CharField(max_length=15000)


class project(models.Model):
    upvotes = models.IntegerField(default = 0, help_text='upvotes')

    project_name = models.CharField(max_length= 100, help_text='project name')

    project_description = models.CharField(max_length= 1000, help_text='project description')

    user_set = models.ForeignKey(Group,default=None)

