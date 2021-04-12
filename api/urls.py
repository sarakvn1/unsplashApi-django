from django.urls import path , include
from .views import ProfileViewSet,UnsplashProfileViewSet, get_authorize_code,get_token,get_user_public_profile,unsplash_callback
from rest_framework import routers
app_name='api'
router=routers.DefaultRouter()
router.register('myprofile',ProfileViewSet)
router.register('unsplash',UnsplashProfileViewSet, basename="unsplash")
urlpatterns = [
    path('',include(router.urls)),
    path('send',get_token),
    path('get',get_authorize_code),
    path('set',unsplash_callback),
    path('profile',get_user_public_profile,name='profile'),
    
   
    ]