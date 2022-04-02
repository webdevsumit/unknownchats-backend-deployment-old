from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

app_name = 'main'

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', testing, name='testing'),
    path('addNewsSellerMail/', addNewsSellerMail, name='addNewsSellerMail'),

    path('accounts/signup/', signup, name='signup'),
    path('accounts/login/', login, name='login'),
    path('accounts/sendForgotPasswordLink/', sendForgotPasswordLink, name='sendForgotPasswordLink'),
    path('getProfile/', getProfile, name='getProfile'),
    path('sendEmailVerificationLink/', sendEmailVerificationLink, name='sendEmailVerificationLink'),
    path('updateEmail/', updateEmail, name='updateEmail'),
    path('verifyEmail/<int:id>/', verifyEmail, name='verifyEmail'),
    path('accounts/resetPass/<int:id>/', resetPass, name='resetPass'),

    path('getFakeProfiles/', getFakeProfiles, name='getFakeProfiles'),
    path('deleteFakeProfile/', deleteFakeProfile, name='deleteFakeProfile'),

    path('getChatingPlatforms/', getChatingPlatforms, name='getChatingPlatforms'),
    path('setTypeInFakeProfile/', setTypeInFakeProfile, name='setTypeInFakeProfile'),
    path('setCollege/', setCollege, name='setCollege'),
    path('setFakeProfile/', setFakeProfile, name='setFakeProfile'),

    path('getEarlierFakeProfiles/', getEarlierFakeProfiles, name='getEarlierFakeProfiles'),
    path('setOnlineToFakeProfiles/', setOnlineToFakeProfiles, name='setOnlineToFakeProfiles'),
    path('getChatBoxesOfFakeProfile/', getChatBoxesOfFakeProfile, name='getChatBoxesOfFakeProfile'),
    path('getOnlineFakeProfiles/', getOnlineFakeProfiles, name='getOnlineFakeProfiles'),
    path('getMessages/', getMessages, name='getMessages'),
    path('addChatBox/', addChatBox, name='addChatBox'),
    path('addMessage/', addMessage, name='addMessage'),
    path('getColleges/', getColleges, name='getColleges'),
]


















