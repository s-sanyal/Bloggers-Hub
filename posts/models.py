from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
class Profile(models.Model):
     user=models.OneToOneField(User,max_length=100,on_delete=models.CASCADE)
     mail=models.CharField(max_length=250,editable=False)
     phone=models.IntegerField(default=0)
     city=models.CharField(max_length=100)
     @receiver(post_save,sender=User)
     def create_user_profile(sender,instance, created, **kwargs):
         if created:
             Profile.objects.create(user=instance)
     @receiver(post_save, sender=User)
     def save_user_profile(sender, instance, **kwargs):
         instance.profile.save()
     def __str__(self):
         return self.user.username

class Topic(models.Model):
    topic_name=models.CharField(max_length=300)
    genre= models.CharField(max_length=100)
    topic_logo=models.CharField(max_length=1000)
    def __str__(self):
        return self.topic_name
class Blogs(models.Model):
    topic= models.ForeignKey(Topic, on_delete=models.CASCADE)
    author=models.ForeignKey(User, null=True, blank=True)
    title=models.CharField(max_length=1000)
    description=models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(auto_now_add=True)
    views=models.IntegerField(default=0,editable=False)
    def __str__(self):
        return self.title
