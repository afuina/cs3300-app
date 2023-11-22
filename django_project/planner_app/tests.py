from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.test import SimpleTestCase
from django.urls import reverse  
from .models import Assignment

# Resource 1: https://learndjango.com/tutorials/django-testing-tutorial
# Resource 2: https://timadey.hashnode.dev/testing-django-apps-effectively

# Create your tests here.

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


# Functional tests using selenium web driver (2) 

# Test to check the following:
# 1: User logs in
# 2: User naviagtes to assignment list view page ("assignments")
# 3: User clicks on "Create Assignment"
# 4: User fills in assignment form information, saves 
# 5: User sees the newly created assignment on the assignment list page
class NewAssignmentTest(LiveServerTestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser',password='testpassword')
        # Create a browser instance
        self.browser = webdriver.Chrome()

    def tearDown(self):
        # Close the browser
        self.browser.quit()

    # Test that a user can create a new assignment using a form
    def test_create_new_assignment(self):
        # 1: user logs in
        self.browser.get(self.live_server_url + '/accounts/login/')
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        password_input.send_keys(Keys.ENTER)

        # 2: user visits assignment list page
        self.browser.get(self.live_server_url + '/assignments/')


        # 3: The user sees a link to create a new assignment and clicks on it
        new_assignment_link = self.browser.find_element(By.LINK_TEXT, 'Add New Assignment')
        new_assignment_link.click()

        # The user sees a form to enter the title and content of the assignment
        title_input = self.browser.find_element(By.NAME, 'title')
        course_input = self.browser.find_element(By.NAME, 'course')
        deadline_input = self.browser.find_element(By.NAME, 'deadline')

        # 4: The user types in the title and content of the assignment
        title_input.send_keys('My first assignment')
        course_input.send_keys('CS 3300')
        deadline_input.send_keys('Today')

        # The user submits the form
        deadline_input.send_keys(Keys.ENTER)

        # 5: The user sees the new assignment on the list page
        self.browser.get(self.live_server_url + '/assignments/')
        new_assignment = self.browser.find_element(By.LINK_TEXT, 'My first assignment')
        self.assertIsNotNone(new_assignment)

# Test to check the following:
# 1: User navigates to log in page
# 2: User clicks the sign up button
# 3: User fills in their information and saves
# 4: User can now log in using newly created account
# 5: User directed to welcome page
class RegisterNewAccountTest(LiveServerTestCase):
    def setUp(self):
        # Create a browser instance
        self.browser = webdriver.Chrome()
    
    def tearDown(self):
        # Close the browser
        self.browser.quit()
    
    # Test that the user can sign up for an account
    def test_create_new_account(self):
        # 1: user navigates to log in page
        self.browser.get(self.live_server_url + '/accounts/login/')

        # 2: user clicks the sign up button
        signup_link = self.browser.find_element(By.LINK_TEXT, 'Sign Up')
        signup_link.click()

        # 3: user fills in their information and submits form
        username_input = self.browser.find_element(By.ID, 'id_username')
        email_input = self.browser.find_element(By.ID, 'id_email')
        password1_input = self.browser.find_element(By.ID, 'id_password1')
        password2_input = self.browser.find_element(By.ID, 'id_password2')

        username_input.send_keys('testuser')
        email_input.send_keys('test@email.com')
        password1_input.send_keys('testpassword')
        password2_input.send_keys('testpassword')

        # The user submits the form
        password2_input.send_keys(Keys.ENTER)

        # 4: User can now log in using newly created account
        self.browser.get(self.live_server_url + '/accounts/login/')
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        password_input.send_keys(Keys.ENTER)

        # 5: User correctly directed to welcome page 
         # Verify that the current URL is the expected welcome page URL
        welcome_page_url = self.live_server_url + '/user/'
        self.assertEqual(self.browser.current_url, welcome_page_url)

        # You can also check for specific elements or content on the welcome page if needed
        welcome_heading = self.browser.find_element(By.TAG_NAME, 'h3')
        self.assertEqual(welcome_heading.text, "Welcome, testuser!") # actual HTML content