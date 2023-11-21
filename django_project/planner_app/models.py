from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Assignment(models.Model):
    PRIORITY = (
        ('!', 'Low Priority'),
        ('!!', 'Regular Priority'),
        ('!!!', 'High Priority')
    )

    # each assignment is assoc to one user,so each user can 
    # only view their assignments in their planner
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    deadline = models.CharField(max_length=200)
    priority = models.CharField(max_length=200, choices=PRIORITY, blank = True)

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.title


    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('assignment-detail', args=[str(self.id)])

