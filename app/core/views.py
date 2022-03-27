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


@api_view(['POST'])
def addNewsSellerMail(request):
    email = request.data['email']
    if email and re.match(EMAIL_REGEX, email):
        mail, _ = NewsSellerEmails.objects.get_or_create(email=email)
        mail.save()
        return Response({"status":"success", "message":"Thank you for subscribing us."})
    return Response({"status":"failed", "message":"Please provide a valid email."})


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


@api_view(['GET'])
def getProfile(request):
    data = {}
    try:
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)
        data['data'] = ProfileSerializer(profile, context={"request", request}).data
        data['status'] = "success"
    except:
        data['status'] = "failed"
        data['error'] = "User not found."
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


@api_view(['GET'])
def sendEmailVerificationLink(request):
    data = {}
    try:
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        if not user.email:
            data['message'] = "Please add your email Id first."
        else:
            isMailSent = sendingMail([user], 'verifyEmail.html')
            if isMailSent:
                data['message'] = "Email is sent"
            else:
                data['message'] = "Something is wrong. Please contact sumit : +917999004229"
            data['status'] = "success"
    except:
        data['error'] = "User with this username is not registered."
        data['status'] = "failed"
    return Response(data)


@api_view(['POST'])
def updateEmail(request):
    data = {}
    try:
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        user.email = request.data["email"]

        profile = Profile.objects.get(user=user)
        profile.isEmailVerified = False
        user.save()
        profile.save()

        isMailSent = sendingMail([user], 'verifyEmail.html')
        if isMailSent:
            data['message'] = "Please check email and confirm your email id."
        else:
            data['message'] = "Something is wrong. Please contact sumit : +917999004229"
        data['status'] = "success"
    except:
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
        # return HttpResponseRedirect("https://unknownchats.com/password-reset-done/")
        return HttpResponse("<h2> Your password has been chaged.<h2>")
    except:
        return HttpResponse("<h2> Sorry something is wrong.<h2>")

def verifyEmail(request, id):
    try:
        profile = Profile.objects.get(user__id=idFormater(id, False))
        profile.isEmailVerified = True
        profile.save()
        # return HttpResponseRedirect("https://unknownchats.com/email-verified/")
        return HttpResponse("<h2> Your email has been verified.<h2>")
    except:
        return HttpResponse("<h2> Sorry something is wrong.<h2>")

@api_view(['POST'])
def setTypeInFakeProfile(request):
    if request.method=='POST':

        chatingPlatform = ChatingPlatform.objects.get(id = request.data['id'])
        
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)
        fakeProfiles = profile.fakeProfiles.filter(isProfileReadyToUse=False)
        if fakeProfiles.exists():
            fakeProfile = fakeProfiles[0]
            fakeProfile.chatingPlatform = chatingPlatform
            fakeProfile.save()
        else:
            fakeProfile = FakeProfile.objects.create(
                chatingPlatform = chatingPlatform
            )
            fakeProfile.save()
            profile.fakeProfiles.add(fakeProfile)
            profile.save()
        return Response({'status':'success'})

    return Response({'status':'failed'})


@api_view(['POST'])
def setCollege(request):
    if request.method=='POST':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user

        college, is_created = College.objects.get_or_create(collegeName = request.data['collegeName'])
        if not is_created:
            college.numberOfTimeSelected += 1

        profile = Profile.objects.get(user=user)
        profile.selectedColleges.add(college)
        profile.save()

        fakeProfiles = profile.fakeProfiles.filter(isProfileReadyToUse=False)
        if fakeProfiles.exists():
            fakeProfile = fakeProfiles[0]
            fakeProfile.selectedCollege = request.data['collegeName']
            fakeProfile.save()
            return Response({'status':'success'})
        else:
            return Response({'status':'failed', "message":"First select the chating platform."})

    return Response({'status':'failed'})


@api_view(['GET'])
def getFakeProfiles(request):
    if request.method=='GET':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)
        fakeProfiles = profile.fakeProfiles.filter(isProfileReadyToUse=False)
        fakeProfileData = {}
        if fakeProfiles.exists():
            fakeProfile = fakeProfiles[0]
            fakeProfileData = FakeProfileSerializer(fakeProfile, context={'request':request}).data

        earlierProfiles = profile.fakeProfiles.filter(isProfileReadyToUse=True, isArchieved=False)
        return Response({
                'status':'success',
                "newProfile":fakeProfileData,
                "earlierProfiles":FakeProfileSerializer(earlierProfiles, many=True, context={'request':request}).data,
            })

    return Response({'status':'failed'})

@api_view(['POST'])
def deleteFakeProfile(request):
    if request.method=='POST':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        fakeProfile = profile.fakeProfiles.get(id=request.data['id'])
        fakeProfile.isArchieved = True
        fakeProfile.save()
        return Response({'status':'success',})
    return Response({'status':'failed'})


@api_view(['POST'])
def setFakeProfile(request):
    if request.method=='POST':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)
        fakeProfile = profile.fakeProfiles.get(id=int(request.data["id"]))
        fakeProfile.displayName = request.data["displayName"]
        fakeProfile.profilePicture = request.FILES.get('profilePicture')
        fakeProfile.isProfileReadyToUse = True
        fakeProfile.isOnline = True
        fakeProfile.save()


        return Response({
                'status':'success',
            })
        
    return Response({'status':'failed'})


@api_view(['GET'])
def getEarlierFakeProfiles(request):
    if request.method=='GET':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)
        earlierProfiles = profile.fakeProfiles.filter(isProfileReadyToUse=True, isArchieved=False)
        return Response({
                'status':'success',
                "earlierProfiles":FakeProfileSerializer(earlierProfiles, many=True, context={'request':request}).data,
            })
       
    return Response({'status':'failed'})


@api_view(['GET'])
def getChatingPlatforms(request):
    if request.method=='GET':
        platforms = ChatingPlatform.objects.all()
        return Response({
                'status':'success',
                "data":ChatingPlatformSerializer(platforms, many=True, context={'request':request}).data,
            })
    return Response({'status':'failed'})


@api_view(['POST'])
def setOnlineToFakeProfiles(request):
    if request.method=='POST':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)

        for tempProfile in profile.fakeProfiles.filter(isOnline = True):
            tempProfile.isOnline = False
            tempProfile.save()

        fakeProfile = profile.fakeProfiles.get(id=int(request.data["id"]))
        fakeProfile.isOnline = True
        fakeProfile.save()
        return Response({
                'status':'success',
            })
       
    return Response({'status':'failed'})


@api_view(['GET'])
def getChatBoxesOfFakeProfile(request):
    if request.method=='GET':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)
        fakeProfile = profile.fakeProfiles.get(isOnline = True)

        chatBoxes = fakeProfile.chatBoxes.filter(isArchieved=False)

        return Response({
                'status':'success',
                "profile":FakeProfileSerializer(fakeProfile, context={'request':request}).data,
                "chatBoxes":ChatBoxSerializer(chatBoxes, many=True, context={'request':request}).data,
            })
       
    return Response({'status':'failed'})


@api_view(['GET'])
def getOnlineFakeProfiles(request):
    if request.method=='GET':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)
        fakeProfile = profile.fakeProfiles.get(isOnline = True)

        if fakeProfile.chatingPlatform.platformNumber=="2":
            onlineProfiles = FakeProfile.objects.filter(isArchieved=False, selectedCollege=fakeProfile.selectedCollege).exclude(id=fakeProfile.id)
        else:
            onlineProfiles = FakeProfile.objects.filter(isArchieved=False).exclude(id=fakeProfile.id)

        return Response({
                'status':'success',
                "profile":FakeProfileSerializer(fakeProfile, context={'request':request}).data,
                "onlineProfiles":FakeProfileSerializer(onlineProfiles, many=True, context={'request':request}).data,
            })
       
    return Response({'status':'failed'})



@api_view(['POST'])
def getMessages(request):
    if request.method=='POST':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)
        fakeProfile = profile.fakeProfiles.get(isOnline = True)

        chatBox = fakeProfile.chatBoxes.filter(isArchieved=False).get(chaters__id=request.data["chaterId"])

        return Response({
                'status':'success',
                "profile":FakeProfileSerializer(fakeProfile, context={'request':request}).data,
                "chatBox":ChatBoxWithMessagesSerializer(chatBox, context={'request':request}).data,
            })
       
    return Response({'status':'failed'})



@api_view(['POST'])
def addChatBox(request):
    if request.method=='POST':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)

        fakeProfile = profile.fakeProfiles.get(isOnline = True)
        fakeProfile2 = FakeProfile.objects.get(id = request.data["chaterAccountId"])

        chater1 = Chater.objects.create(name=fakeProfile.displayName)
        chater2 = Chater.objects.create(name=fakeProfile.displayName)

        chatBox = ChatBox.objects.create()
        chatBox.chaters.add(chater1)
        chatBox.chaters.add(chater2)

        fakeProfile.chatBoxes.add(chatBox)
        fakeProfile2.chatBoxes.add(chatBox)

        fakeProfile.save()
        fakeProfile2.save()

        return Response({
                'status':'success',
            })
       
    return Response({'status':'failed'})


@api_view(['POST'])
def addMessage(request):
    if request.method=='POST':
        user = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]).user
        profile = Profile.objects.get(user=user)

        chatBox = ChatBox.objects.get(id = request.data["chatBoxId"])

        message = Message.objects.create(
            chater = request.data["chater"],
            message = request.data["message"]
        )

        chatBox.messages.add(message)
        chatBox.save()
        message.save()

        return Response({
                'status':'success',
            })
       
    return Response({'status':'failed'})


