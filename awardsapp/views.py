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

#class-based developed api end-points
class ProfileList(APIView):
    def get(self,request,format=None):
        profiles=Profile.objects.all()
        serializers=ProfileSerializer(profiles,many=True)
        return Response(serializers.data)

class ProjectsList(APIView):
    def get(self,request,format=None):
        projects=Projects.objects.all()
        serializers=ProjectsSerializer(projects,many=True)
        return Response(serializers.data)


@login_required(login_url='login')
def project(request, project_id):
    project = Projects.objects.get(pk=project_id)
    ratings = Ratings.project_votes(project.id)
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project
            rate.save()
            post_ratings = Ratings.objects.filter(project=project)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
        
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingForm()
    params = {
        'project':project,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'project.html', params)