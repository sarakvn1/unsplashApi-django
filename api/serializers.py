from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Profile ,UnsplashProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','password','first_name','last_name','email')
        extra_kwargs={'password':{'write_only':True,'required':True}}
    # we have to override tha create
    # method because the 'write_only' and 
    # 'required' will store the password as
    # a normal field and will not hashed
   
    # it will hash the password and create user 
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        # it will create token automatically for each user
        token=Token.objects.create(user=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Profile
        fields=('id','user','first_name','last_name','access_token') 

class UnsplashProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=UnsplashProfile
        fields=('id','profile','string_id','numeric_id','username','twitter_username','instagram_username','followers_count','following_count') 