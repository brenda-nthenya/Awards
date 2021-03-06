from django.contrib.auth.models import User
from django.db.models import fields
from .models import Ratings,Profile,Projects
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
  email=forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
  class Meta:
    model = User
    fields=['username','email','password1','password2']

class AddProjectForm(ModelForm):
  class Meta:
    model = Projects
    fields = ['name','description','project_image','urls']

class RatingForm(ModelForm):
  class Meta:
    model = Ratings
    fields = ['design','usability','content']

class UpdateUserForm(ModelForm):
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
  class Meta:
    model = User
    fields = ['username', 'email']

class UpdateProfile(ModelForm):
  class Meta:
    model = Profile
    fields = ['name','location','bio','email']