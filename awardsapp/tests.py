
# Create your tests here.
from django.test import TestCase
from .models import *


class TestProfile(TestCase):
    def setUp(self):
        self.user = User(id=1, username='Brenda', password='yeepie')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()


class ProjectTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='brenda')
        self.project =Projects.objects.create(id=1, name='sample project', project_image='https://imagesvc.meredithcorp.io/v3/mm/image?q=60&c=sc&poi=%5B1020%2C471%5D&w=2000&h=1000&url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F23%2F2021%2F12%2F17%2Fbreathable-nail-polish-2000.jpg', 
                                        description='NailPolish', user=self.user, url='http://ur.coml')

    def test_instance(self):
        self.assertTrue(isinstance(self.proj,Projects))

    def test_save_project(self):
        self.project.save_post()
        project =Projects.objects.all()
        self.assertTrue(len(project) > 0)

    def test_get_project(self):
        self.post.save()
        project =Projects.all_posts()
        self.assertTrue(len(project) > 0)

    def test_search_project(self):
        self.post.save()
        project =Projects.search_project('test')
        self.assertTrue(len(project) > 0)

    def test_delete_project(self):
        self.project.delete_post()
        project =Projects.search_project('test')
        self.assertTrue(len(project) < 1)


class RatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='brenda')
        self.project =Projects.objects.create(id=1, name='test post', project_image='https://ucarecdn.com/0ccf61ff-508e-46c6-b713-db51daa6626e', description='desc',
                                        user=self.user, url='http://ur.com')
        self.rating = Ratings.objects.create(id=1, design=6, usability=7, content=9, user=self.user, proj=self.project)

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Ratings))

    def test_save_rating(self):
        self.rating.save_rating()
        rating = Ratings.objects.all()
        self.assertTrue(len(rating) > 0)

    def test_get_project_rating(self, id):
        self.rating.save()
        rating = Ratings.get_ratings(project_id=id)
        self.assertTrue(len(rating) == 1)
