from . import views
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

urlpatterns=[
    path('', views.index, name='index'),
    path('signup/',views.signup,name='signup'),
    path('project/<int:project_id>/',views.project,name='project'),
    path('edit_profile/<int:profile_id>/', views.edit_profile, name='edit_profile'),
    path('add_project/',views.add_project,name='add_project'),
    path('rate_project/<int:project_id>/',views.rate_project,name = 'rate_project'),
    path('search_project/',views.search_project,name='search_project'),
    path('profile/<int:profile_id>/',views.profile,name='profile'),
    path('api/profiles/',views.ProfileList.as_view()),
    path('api/projects/',views.ProjectsList.as_view()),
    path('api/profile/',views.ProfilesList),
    path('api/project/',views.ProjectList),
   ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)