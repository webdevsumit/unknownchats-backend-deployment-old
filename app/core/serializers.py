from django.db.models import fields
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'is_superuser'
        )
        extra_kwargs={
            'password':{'write_only':True}
        }

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"


class ChatingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatingPlatform
        fields = "__all__"


class FakeProfileSerializer(serializers.ModelSerializer):
    chatingPlatform = ChatingPlatformSerializer()
    class Meta:
        model = FakeProfile
        fields = ["id", "displayName", "selectedCollege", "profilePicture", "isOnline", "chatingPlatform"]


class ChaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chater
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class ChatBoxWithMessagesSerializer(serializers.ModelSerializer):
    chaters = ChaterSerializer(many=True)
    messages = MessageSerializer(many=True)
    class Meta:
        model = ChatBox
        fields = "__all__"

class ChatBoxSerializer(serializers.ModelSerializer):
    chaters = ChaterSerializer(many=True)
    class Meta:
        model = ChatBox
        fields = ["id", "chaters", "createdAt"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "mobileNo",
            "isEmailVerified",
            "isEmailNotificationAllowed",
            ]