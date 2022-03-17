from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

app_name = 'main'

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', testing, name='testing'),

    path('accounts/signup/', signup, name='signup'),
    path('accounts/login/', login, name='login'),
    path('accounts/sendForgotPasswordLink/', sendForgotPasswordLink, name='sendForgotPasswordLink'),
    path('accounts/resetPass/<int:id>/', resetPass, name='resetPass'),

]


















