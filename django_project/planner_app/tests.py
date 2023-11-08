from django.test import TestCase

# Create your tests here.
from django.test import SimpleTestCase
from django.urls import reverse  

# Resource: https://learndjango.com/tutorials/django-testing-tutorial

class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "planner_app/index.html")

    def test_template_content(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, "<h1>My Planner</h1>")
        self.assertNotContains(response, "Not on the page")

# Remove "SimpleTestCase" and replace with "TestCase" class because the 
# simple one cannot access the database and will be unable to test if the
# model list view works. 
class AssignmentListTests(TestCase):  
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/assignments/") # should match url in urls.py
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("assignments")) # should match the name in urls.py
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("assignments"))
        self.assertTemplateUsed(response, "planner_app/assignment_list.html")

    def test_template_content(self):
        response = self.client.get(reverse("assignments"))
        self.assertContains(response, "<h1>Assignment List</h1>") # should match your template
        self.assertNotContains(response, "Should not be here!")