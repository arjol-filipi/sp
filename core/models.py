from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
import datetime
import secrets

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trust_key = models.CharField(max_length=50,null=True,blank=True,)
    monitor = models.BooleanField(default=False)
    trusted_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True,related_name='worker',default=None)
    def __str__(self):
        return self.user.username

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
class Emplyee(models.Model):
    name = models.CharField( max_length = 255)
    position = models.CharField(max_length= 255,blank=True,null=True)
    at_work = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    card_id = models.CharField( max_length = 255,default=secrets.token_urlsafe(10))
    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = 'Emplyee'
        verbose_name_plural = 'Emplyees'

class Event(models.Model):
    emplyee = models.ForeignKey(Emplyee, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    time_added = models.DateTimeField(default=datetime.datetime.now())
    time = models.DateTimeField(default=datetime.datetime.now())
    enter = models.BooleanField(default=True)
    def __str__(self):
        return self.emplyee.name

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'