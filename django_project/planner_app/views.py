from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Assignment
from .forms import AssignmentForm

# Create your views here.
def index(request):
    # Render the HTML template index.html with the data
    # in the context variable. 

    return render(request, 'planner_app/index.html')

# method to create an assignment
def createAssignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            # Create a new assignment object but don't save it to the database yet
            new_assignment = form.save(commit=False)
            
            # You can perform additional processing here if needed
            
            # Save the assignment to the database
            new_assignment.save()
            
            # Optionally, you can redirect to a page showing the created assignment
            return redirect('assignment-detail', pk=new_assignment.pk)  # Define 'assignment_detail' URL pattern in your urls.py
    else:
        form = AssignmentForm()
    
    return render(request, 'planner_app/assignment_form.html', {'form': form})

# method to update/edit an assignment
def updateAssignment(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment-detail', assignment.id)  # Redirect to the assignment detail page
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'planner_app/assignment_update_form.html', {'form': form, 'assignment': assignment})

# method to delete an assignment
def deleteAssignment(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)

    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments')  # Redirect to the portfolio detail page

    return render(request, 'planner_app/assignment_confirm_delete.html', {'assignment': assignment})

class AssignmentListView(generic.ListView):
    model = Assignment  # Assignment model
    template_name = 'planner_app/assignment_list.html'  # Template for listing assignments
class AssignmentDetailView(generic.DetailView):
    model = Assignment  # Assignment model
    template_name = 'planner_app/assignment_detail.html'  # Template for displaying assignment details