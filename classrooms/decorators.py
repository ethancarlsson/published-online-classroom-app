from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Classroom
# decorators based on the Dennis Ivy video:  
# User Role Based Permissions & Authentication | Django (3.0) Crash Course Tutorials (pt 15)

def already_authenticated_user(view_func):
    '''checks to see is already logged in and redirects them away from login and register pages.'''
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users():
    '''Makes sure students from other groups cannot access the pages or classes they are not signed up for'''
    def decorator(view_func):
        def wrapper_func(request, classroom_id, *args, **kwargs):
            group = None
            all_user_groups = None
            classroom_being_entered = None
            if request.user.groups.exists():
                group = request.user.groups.all()
                all_user_groups = [str(name.name) for name in group]
                classroom_being_entered = Classroom.objects.get(id=classroom_id)


            if str(classroom_being_entered) in all_user_groups:
                return view_func(request, classroom_id, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def restricted_access(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = None
            if request.user.groups.exists():
                groups = request.user.groups.all()
                groups = [group.name for group in groups] 
            
            if allowed_roles[0] in groups:
                return view_func(request, *args, **kwargs)

            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator
    