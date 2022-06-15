from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from rest_framework import serializers
from .forms import *
import datetime as dt
from django.http.response import Http404, HttpResponse
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer,ProjectsSerializer


# Create your views here.

def index(request):
    date=dt.date.today()
    try:
        projects=Projects.get_all_projects()
    except Projects.DoesNotExist:
        raise Http404()

    project_ratings=projects.order_by('-ratings__average_rating')
    best_rating=None
    best_votes=None
    if len(project_ratings)>=1:
        best_rating=project_ratings[0]
        ratings=Ratings.project_votes(best_rating.id)

    context = {
        "date":date,
        "highest_vote":best_votes,
        "projects":projects,
        "highest_rating":best_rating
    }
    return render(request,'index.html',context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})