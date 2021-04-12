from django.shortcuts import render
import requests
import re
from uuid import uuid4
from requests import Session
from bs4 import BeautifulSoup as bs
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
import urllib
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Profile ,UnsplashProfile
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UserSerializer,ProfileSerializer,UnsplashProfileSerializer
from rest_framework.response import Response
from rest_framework import viewsets,status

# Create your views here.
# def unsplash_callback(request):
#         code=request.GET.get('code')
#         print("this is code",code)
#         access_token=get_token(code)
#         user=request.user
#         user_instance=User.objects.get(id=user.id)
#         user_profile=Profile.objects.get(user=user_instance)
#         user_profile.access_token=access_token
#         user_profile.save()
#         print("this is unsplsh",access_token)
        
#         return HttpResponseRedirect(reverse('profile'))

def unsplash_callback(request):
        code=request.GET.get('code')
        print("this is code",code)
        access_token=get_token(code)
        user=request.user
        user_instance=User.objects.get(id=user.id)
        user_profile=Profile.objects.get(user=user_instance)
        user_profile.access_token=access_token
        user_profile.save()
        print("this is unsplsh",access_token)
        
        return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/unsplash/public_profile/")

def get_authorize_code(request):
    client_id="i6CKPHRCccFRJTfG8-XeZ5ZrQAHmdvWB6FhWxKI8El8"
    REDIRECT_URI="http://127.0.0.1:8000/set"
    params={
        "client_id":client_id,
        "response_type":"code",
        "redirect_uri":REDIRECT_URI,
        "scope":"public"
    }
    authurl="https://unsplash.com/oauth/authorize?"+ urllib.parse.urlencode(params)
    
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        }
    # x=redirect(authurl)
    # print("this is xxxx:",x)
    return redirect(authurl)

    
    
  


def get_token(authorize_code):
    client_id="i6CKPHRCccFRJTfG8-XeZ5ZrQAHmdvWB6FhWxKI8El8"
    client_secret="m4AEmg5QdBHNIZvz9THzNLjXLviIWN4t0i4E3RJ9GYk"
    REDIRECT_URI="http://127.0.0.1:8000/set"
    redirect_uri=REDIRECT_URI
    url="https://unsplash.com/oauth/token"

    data={  'client_id':client_id,
            'client_secret':client_secret,
            'redirect_uri':redirect_uri,
            'code':authorize_code,
            'grant_type':'authorization_code'}

    response=requests.post(url,data=data)
    res=json.loads(response.content.decode('utf-8'))

    try:
        access_token=res["access_token"]
    except:
        access_token=res
        # print(res)
    return access_token

def get_user_public_profile(request):

    
    user=request.user
    user_instance=User.objects.get(id=user.id)
    user_profile=Profile.objects.get(user=user_instance)
    access_token=user_profile.access_token
    if access_token:
        print("this is access token %s" %access_token)
        header_dict={"Authorization": "Bearer %s" %access_token}
        url="https://api.unsplash.com/me"
        response=requests.get(url,headers=header_dict)
        
        res=json.loads(response.content.decode('utf-8'))
        return HttpResponse(f"this is response {res}")
    else:
        return redirect('/get')



class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    
    

    

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)


    
    

class UnsplashProfileViewSet(viewsets.ModelViewSet):
    queryset = UnsplashProfile.objects.all()
    serializer_class = UnsplashProfileSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)


    
    @action(detail=False,methods=['GET'])
    def public_profile(self,request):
       
        try:
            user=request.user
            print("id",user.id)
            user_instance=User.objects.get(id=user.id)
            user_profile=Profile.objects.get(user=user_instance)
            access_token=user_profile.access_token
            if access_token:
                print("this is access token %s" %access_token)
                header_dict={"Authorization": "Bearer %s" %access_token}
                url="https://api.unsplash.com/me"
                res=requests.get(url,headers=header_dict)
                
                unsplash_api_response=json.loads(res.content.decode('utf-8'))
                
                # response=UnsplashProfileSerializer(unsplash_api_response,many=True)
                # print("------",response.data)
                return Response(unsplash_api_response,status=status.HTTP_200_OK)
            else:
                return redirect('/get')
        except:
                response={'message':'sorry nothing found'}
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        


    # return HttpResponse( "access token:%s" %access_token)


        # response=requests.get('http://127.0.0.1:8000/get')
        # print(response.content)
        # access_token=user_profile.access_token
        # if access_token:
        #     header_dict={"Authorization": "Bearer %s" %access_token}
        #     url="https://api.unsplash.com/me"
        #     response=requests.get(url,headers=header_dict)
        #     res=json.loads(response.content.decode('utf-8'))
        #     return HttpResponse(f"this is response {res}")
        # else:
        #     return HttpResponse(f"this is response ")

# def get_user_image

  # res=json.loads(response.content.decode('utf-8'))
    
    
    # except login:
    #     loginurl="https://unsplash.com/login"
    #     response=requests.get(loginurl)
    #     bs_content = bs(response.content, "html.parser")
    #     token = bs_content.find("input", {"name":"authenticity_token"})["value"]
    #     login_data = {"user[email]":"skuisbluex@hotmail.com","user[password]":"456321sky","utf8":True, "authenticity_token":token,"commit":"Login"}
    #     response=requests.post(loginurl,login_data)
    # with Session() as s:
    #     authurl=f"https://unsplash.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=public+read_user+write_user+read_photos+write_photos+write_likes+write_followers+read_collections+write_collections"
    #     url="https://unsplash.com/login"
    #     url_code="https://unsplash.com/oauth/authorize/"
    #     
       
    #     res = s.get(authurl)
    #     next_page=bs(res.content, "html.parser")
    #     continue_button=next_page.find("input",{"type":"submit"})["value"]
    #     sending_data={"authenticity_token":token,"commit":continue_button,"client_id":client_id,"redirect_uri":redirect_uri,"response_type":"code","scope":"public"}
        
    #     result_code = s.post(url_code,sending_data)
    #     code_page=bs(result_code.content, "html.parser")
        
    #     code=code_page
        # clean = re.compile('<.*?>')
        # return re.sub(clean, '', code)

        
        
        
    # return HttpResponse(f"this is code: {code}")