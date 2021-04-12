from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    access_token=models.CharField(max_length=100,blank=True,null=True)

class UnsplashProfile(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    string_id=models.CharField(max_length=20)
    numeric_id=models.IntegerField()
    username=models.CharField(max_length=50)
    twitter_username=models.CharField(max_length=50)
    portfolio_url=models.CharField(max_length=1000)
    instagram_username=models.CharField(max_length=50)
    total_collections=models.IntegerField()
    total_likes=models.IntegerField()
    total_photos=models.IntegerField()
    followers_count=models.IntegerField()
    following_count=models.IntegerField()
