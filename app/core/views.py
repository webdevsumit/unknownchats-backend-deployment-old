from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,login,logout)
from django.db.models import Q
import datetime
from datetime import timezone
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import *

import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


def idFormater(data, idToComplex=True):
    import datetime
    x = datetime.datetime.now()
    formater = 9713751690*x.year*x.month*x.day
    if idToComplex:
        formatedID = formater*int(data)
        return formatedID
    else:
        return int(int(data)/formater)


@api_view(['GET'])
def testing(request):
    return Response({"status":"success", "hey":"Do you need any help?"})


@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        
        user_exist = User.objects.filter(username=request.data['username']).exists()
        if user_exist:
            return Response({'error':'Username already exists.'})
            
        user_data = UserSerializer(data=request.data)
        if user_data.is_valid(raise_exception=True):
            user = user_data.create(user_data.validated_data)

            user.set_password(request.data['password'])
            user.save()

            profile = Profile.objects.create(user=user)
            profile.save()

            user_ = authenticate(user_data.validated_data)
            if user_ is not None:
                user.last_login = datetime.datetime.now()
                user.save()
                login(request,user_)
            
            token, _  = Token.objects.get_or_create(user_id=user.id)
            return Response({'status':'success',"token": token.key})
    return Response({'status':'failed'})


@api_view(['POST'])
def login(request):
    username = request.data['username']
    users = User.objects.filter(username=username)
    if not users.exists():
        return Response({'status':'failed','error':'User with this username not found.'})
    user = users[0]
    if not user.check_password(request.data['password']):
        return Response({'status':'failed','error':'Password is incorrect.'})
    
    data = {'username':user.username}
    token, _  = Token.objects.get_or_create(user_id=user.id)
    data['token'] = token.key
    data['status'] = "success"
    return Response(data)


def sendingMail(users, tempFile, password=''):
    subject = 'Sumit from Unknown Chats'
    for user in users:
        html_message = render_to_string(tempFile, {'first_name': user.username, 'id': idFormater(user.id), 'password':password})
        plain_message = strip_tags(html_message)

        try:
            mail.send_mail(subject, plain_message, 'sumit.unknownchats@gmail.com', [user.email], html_message=html_message)
            return True
        except:
            print("error in sending email.")
            return False


@api_view(['POST'])
def sendForgotPasswordLink(request):
    data = {}
    if User.objects.filter(username=request.data['username']).exists():
        user = User.objects.get(username=request.data['username'])
        if not user.email:
            data['message'] = "Email is not added to your account. Sorry you cannot recover your account."
        else:
            profile = Profile.objects.get(user=user)
            profile.tempPassword = request.data['password']
            profile.save()

            isMailSent = sendingMail([user], 'forgotpass.html',password=profile.tempPassword)

            if isMailSent:
                data['message'] = "Email is sent"
            else:
                data['message'] = "Something is wrong. Please contact sumit : +917999004229"
            data['status'] = "success"
    else:
        data['error'] = "User with this username is not registered."
        data['status'] = "failed"
    return Response(data)


def resetPass(request, id):
    try:
        profile = Profile.objects.get(user__id=idFormater(id, False))
        profile.user.set_password(profile.tempPassword)
        profile.user.save()
        profile.isEmailVerified = True
        profile.save()
        return HttpResponseRedirect("https://unknownchats.com/")
    except:
        return HttpResponse("<h2> Sorry something is wrong.<h2>")

