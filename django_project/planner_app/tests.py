from django.test import TestCase, override_settings
from django.contrib.auth.models import User
# Create your tests here.
from django.test import SimpleTestCase
from django.urls import reverse  
from .models import Assignment

# Resource 1: https://learndjango.com/tutorials/django-testing-tutorial
# Resource 2: https://timadey.hashnode.dev/testing-django-apps-effectively


# Integration test for homepage view (1) 
class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):  
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200) # check page accessed correctly
        self.assertTemplateUsed(response, "planner_app/index.html") # check correct template used
        self.assertContains(response, "<h1>My Planner</h1>") # should match template

# Integration test for assignment list view (1)
# Remove "SimpleTestCase" and replace with "TestCase" class because the 
# simple one cannot access the database and will be unable to test if the
# model list view works. 
class AssignmentListTests(TestCase):  
    def setUp(self):
        # create a test user to simulate logging in
        self.user = User.objects.create_user(username='testuser',password='testpassword')
        # log in the test user
        self.client.login(username='testuser', password='testpassword')

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/assignments/") # should match url in urls.py
        self.assertEqual(response.status_code, 200)

    def test_assignment_list_view(self):  
        response = self.client.get(reverse("assignments")) # should match the name in urls.py
        self.assertEqual(response.status_code, 200) # check page accessed correctly
        self.assertTemplateUsed(response, "planner_app/assignment_list.html") # check correct template used
        self.assertContains(response, "<h1>Assignment List</h1>") # should match your template

#Integration test for assignment detail view (1)
class AssignmentDetailTests(TestCase): 
    def setUp(self):
        # create a test user to simulate logging in
        self.user = User.objects.create_user(username='testuser',password='testpassword')
        # create a test assignment to simulate assignment detail view)
        self.assignment = Assignment.objects.create(
            user=self.user, 
            title='Test Assignment',
            course='Test',
            deadline='Test')
        # Log in the test user & check detail view for test assignment 
        self.client.login(username='testuser', password='testpassword')

    """def test_url_exists_at_correct_location(self):
        # Log in the test user & check detail view for test assignment 
        self.client.login(username='testuser', password='testpassword')
        pk = self.assignment.pk
        response = self.client.get("/assignment/", args = [pk]) # should match url in urls.py
        self.assertEqual(response.status_code, 200)
        """

    def test_assignment_detail_view(self):  
        response = self.client.get(reverse("assignment-detail", args=[self.assignment.pk])) # should match the name in urls.py
        self.assertEqual(response.status_code, 200) # check page accessed correctly 
        self.assertTemplateUsed(response, "planner_app/assignment_detail.html") # check correct template used
        self.assertContains(response, f"<h1>Assignment Name: {self.assignment.title}</h1>") # should match your template


# Unit Tests
#class AssignmentTests(TestCase):
