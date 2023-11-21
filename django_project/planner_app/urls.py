from django.urls import path, include
from . import views


urlpatterns = [
#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
    path('', views.index, name='index'),
    path('assignments/', views.AssignmentListView.as_view(), name= 'assignments'),
    path('assignment/<int:pk>', views.AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignments/create_assignment/', views.createAssignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/update_assignment/', views.updateAssignment, name='update_assignment' ),
    path('assignment/<int:assignment_id>/delete_assignment/', views.deleteAssignment, name='delete_assignment' ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.registerPage, name = 'register_page'),
    path('user/', views.userPage, name='user_page'),
   
]
