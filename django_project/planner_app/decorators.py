from django.http import HttpResponse
from django.shortcuts import redirect

# I could not get this code to work - essentially it is supposed to limit access
# for certain groups ie customers vs internal, but this is irrelevant for the planner
# app because we only have one group of users. To implement this decorator, place this above a 
# view function: @allowed_users(allowed_roles=['user_role']), also: from .decorators import allowed_users

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('role', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('You are not authorized to view this page. ')
            return redirect('login')
        return wrapper_func
    return decorator 
        