from http import server
from rest_framework import serializers
from django.db.models import fields
from django.contrib.auth.models import User


from .models import *

from django.db import models

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id',
                  'user',
                  'profile_pic',
                  'bio',
                  'email',
                  'url',
                  'location')
