from django.forms import ModelForm
from .models import Assignment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#create class for assignment form
class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields =('title', 'course', 'deadline', 'priority')
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

"""class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
"""