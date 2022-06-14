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

class ProjectsSerializer(serializers.ModelSerializer):
      class Meta:
        model = Projects
        fields=('id',
                'name',
                'description',
                'project_image',
                'urls',
                'pub_date')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    posts = ProjectsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'profile', 'posts']