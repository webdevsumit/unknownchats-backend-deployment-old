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
