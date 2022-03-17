from django.db import models
from django.contrib.auth.models import User

class College(models.Model):
    collegeName = models.CharField(max_length=50,default='Open World')
    numberOfTimeSelected = models.IntegerField(default=1)
    
    def __str__(self):
        return self.collegeName

class ChatingPlatform(models.Model):
    platformName = models.CharField(max_length=50,default='Open World')
    platformNumber = models.CharField(max_length=50)
    
    def __str__(self):
        return self.platformName

class Chater(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Message(models.Model):
    chater = models.CharField(max_length=300)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)
    isArchieved = models.BooleanField(default=False)

    def __str__(self):
        return self.chater

class ChatBox(models.Model):
    chaters = models.ManyToManyField(Chater, blank=True)
    messages = models.ManyToManyField(Message, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    isArchieved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.createdAt)

class FakeProfile(models.Model):
    displayName = models.CharField(max_length=300)
    isProfileReadyToUse = models.BooleanField(default=False)
    chatingPlatform = models.ForeignKey(ChatingPlatform, on_delete=models.PROTECT)
    selectedCollege = models.CharField(max_length=20, default='', blank=True)
    profilePicture = models.ImageField(upload_to='profilePicture', default='images/logo.png')
    isOnline = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now=True)
    chatBoxes = models.ManyToManyField(ChatBox, blank=True)
    isArchieved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.displayName


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobileNo = models.CharField(max_length=12,default='')
    isEmailVerified = models.BooleanField(default=False)
    isEmailNotificationAllowed = models.BooleanField(default=True)
    selectedColleges = models.ManyToManyField(College, blank=True)
    tempPassword = models.CharField(max_length=50, default="12345678")
    fakeProfiles = models.ManyToManyField(FakeProfile, blank=True)
    

    def __str__(self):
        return self.User.username
