from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Assignment
from .forms import AssignmentForm, CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
def index(request):
    # Render the HTML template index.html with the data
    # in the context variable. 

    return render(request, 'planner_app/index.html')

# method to create an assignment
@login_required(login_url='login')
def createAssignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            # Create a new assignment object but don't save it to the database yet
            new_assignment = form.save(commit=False)
            
            # You can perform additional processing here if needed
            new_assignment.user = request.user # Associate the assignment with the logged-in user
            # Save the assignment to the database
            new_assignment.save()
            
            # Optionally, you can redirect to a page showing the created assignment
            return redirect('assignment-detail', pk=new_assignment.pk)  # Define 'assignment_detail' URL pattern in your urls.py
    else:
        form = AssignmentForm()
    
    return render(request, 'planner_app/assignment_form.html', {'form': form})

# method to update/edit an assignment
@login_required(login_url='login')
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
@login_required(login_url='login')
def deleteAssignment(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)

    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments')  # Redirect to the portfolio detail page

    return render(request, 'planner_app/assignment_confirm_delete.html', {'assignment': assignment})

# method to sign up for an account
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        
    return render(request, 'registration/register.html', {'form': form})

# creates the page for the user once they are logged in
@login_required(login_url='login')
def userPage(request):
    print("Logging you in...")
    context = {'user': request.user}
    return render(request, 'planner_app/user.html', context)


class AssignmentListView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    model = Assignment  # Assignment model
    template_name = 'planner_app/assignment_list.html'  # Template for listing assignments

    # filter the assignment list for only those associated with the current user - this way they 
    # cannot view anyone else's assignments
    def get_queryset(self):

        # get all assignments for the current user
        assignments = Assignment.objects.filter(user=self.request.user)

        return assignments

class AssignmentDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'login'
    model = Assignment  # Assignment model
    template_name = 'planner_app/assignment_detail.html'  # Template for displaying assignment details

     # filter the assignment detail for only those associated with the current user
    def get_queryset(self):
        return Assignment.objects.filter(user=self.request.user)

