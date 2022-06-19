from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    # profile_pic=models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio=models.TextField()
    location=models.CharField(max_length=50)
    email=models.EmailField()
    url=models.URLField()
    name = models.CharField(blank=True, max_length=120)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
            self.save()
    
    def delete_profile(self):
        self.delete()

class Projects(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    project_image=models.ImageField(upload_to='project_images')
    urls=models.URLField()
    pub_date=models.DateTimeField(auto_now_add=True)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    voters = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['-pub_date']

    def save_project(self):
        self.save()
  
    def delete_project(self):
        self.delete()

    def voters_num(self):
        return self.voters.count()

    @classmethod
    def get_all_projects(cls):
        return cls.objects.all()

    @classmethod
    def get_project(cls,id):
        return Projects.objects.get(id=id)

    @classmethod
    def search_project(cls,name):
        return cls.objects.filter(name__icontains=name)

    @classmethod
    def user_projects(cls,profile):
        return cls.objects.filter(profile=profile)

class Ratings(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    design = models.IntegerField(choices=rating,blank=False)
    usability = models.IntegerField(choices=rating,blank=False)
    content = models.IntegerField(choices=rating,blank=False)
    rater = models.ForeignKey(Profile,on_delete=models.CASCADE)
    projects=models.ForeignKey(Projects,on_delete=models.CASCADE, related_name='ratings')
    pub_date=models.DateTimeField(auto_now_add=True)
    design_average=models.FloatField(default=0)
    usability_average=models.FloatField(default=0)
    content_average=models.FloatField(default=0)
    average_rating=models.FloatField(default=0)

    def __str__(self):
        return self.project

    def save_rating(self):
        self.save()
  
    def delete_rating(self):
        self.delete()

    @classmethod
    def project_votes(cls,project):
        return cls.objects.filter(projects=project)

    @classmethod
    def project_voters(cls,rater):
        return cls.objects.filter(rater=rater)

    class Meta:
        ordering=['pub_date']