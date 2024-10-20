
from django.db import models
from django.contrib.auth.models import User




class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text


class Entry(models.Model):
    """Something specific learned about a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a simple string representing the entry."""
        return f"{self.text[:50]}..."

class Profile(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio=models.TextField()
    profile_pic=models.ImageField(upload_to='images/',null=True, blank=True,)
    email=models.CharField(max_length=255, null=True, blank=True)
    vsco_url=models.CharField(max_length=255, null=True, blank=True)
    insta_url=models.CharField(max_length=255, null=True, blank=True)
    snapchat_url=models.CharField(max_length=255, null=True, blank=True)
    First_Name=models.CharField(max_length=255, null=True, blank=True)
    Last_Name=models.CharField(max_length=255, null=True, blank=True)
    
    # The field representing the users following this profile
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    # The field representing the profiles this user is following
    following = models.ManyToManyField('self', symmetrical=False, related_name='followed_by', blank=True)
    


    def __str__(self):
        """Return a string representation of the model."""
        return str(self.user)

    

