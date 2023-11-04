from django.forms import ModelForm
from .models import Assignment


#create class for assignment form
class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields =('title', 'course', 'deadline', 'priority')
