from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from rest_framework import serializers

from .email import send_welcome_email
from .forms import *
import datetime as dt
from django.urls import reverse
from django.http.response import Http404, HttpResponse
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer,ProjectsSerializer


# Create your views here.

def index(request):
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

@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateProfile(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateProfile(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'edit.html', params)

@login_required(login_url='login')
def rate_project(request, project_id):
    if request.method == "POST":
        form = RatingForm(request.POST)
        project = Projects.objects.get(pk=project_id)
        current_user = request.user
        try:
            user = User.objects.get(pk=current_user.id)
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Http404()
        if form.is_valid():
            ratings = form.save(commit=False)
            ratings.rater = profile
            ratings.projects = project
            ratings.save()
        return HttpResponseRedirect(reverse('project', args=[int(project.id)]))
    else:
        form = RatingForm()
    return render(request, 'project.html', {"form": form})


@login_required
def profile(request,profile_id):
    try:
        user=User.objects.get(pk=profile_id)
        profile=Profile.objects.get(user=user)
        profile_projects=Projects.user_projects(profile)
        projects_stats=profile_projects.count()
        project_ratings = Ratings.objects.filter(projects=profile_projects.first())
        if len(project_ratings) >= 1:
            votes=[i.average_rating for i in project_ratings]
            total_ratings=sum(votes)
            average=total_ratings/len(profile_projects)

        context = {
            "profile":profile,
            "profile_projects":profile_projects,
            "projects_stats":projects_stats,
            "ratings":total_ratings,
            "average":average
        }
        return render(request,'profile.html', context)
    
    except Profile.DoesNotExist:
        raise Http404()
        
    # return render(request,'profile/profile.html',{"profile":profile,"profile_projects":profile_projects,"projects_stats":projects_stats})

def search_project(request):
    if request.method == 'GET':
        name = request.GET.get("name")
        results = Projects.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any project category"
    return render(request, 'results.html', {'message': message})


def email(request):
    user = request.user
    email = user.email
    name = user.username
    send_welcome_email(name, email)
    return redirect(index)

@login_required
def add_project(request):
  if request.method == "POST":
    form = AddProjectForm(request.POST,request.FILES)
    user=request.user
    try:
      profile=Profile.objects.get(user=user)
    except Profile.DoesNotExist:
      raise Http404()
    if form.is_valid():
      new_project=form.save(commit=False)
      new_project.profile = profile
      new_project.save()
    return redirect('index')
  else:
    form=AddProjectForm()
  return render(request,'add_project.html',{"form":form})