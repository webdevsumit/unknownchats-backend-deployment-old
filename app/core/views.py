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

@api_view(['GET'])
def testing(request):
    return Response({"status":"success"})