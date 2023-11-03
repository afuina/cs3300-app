from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Assignment

# Create your views here.
def index(request):
    # Render the HTML template index.html with the data
    # in the context variable. 

    return render(request, 'planner_app/index.html')

class AssignmentListView(generic.ListView):
    model = Assignment  # Assignment model
    template_name = 'planner_app/assignment_list.html'  # Template for listing assignments
class AssignmentDetailView(generic.DetailView):
    model = Assignment  # Assignment model
    template_name = 'planner_app/assignment_detail.html'  # Template for displaying assignment details