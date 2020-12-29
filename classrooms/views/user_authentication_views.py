from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group

from classrooms.decorators import already_authenticated_user
from classrooms.forms import CreateUserForm
from classrooms.models import Classroom

from . import home

@already_authenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #add user to the "anyone can sign up group"
            anyone_can_signup = Group.objects.get(name='Anyone can sign up')
            anyone_can_signup.user_set.add(user)

            #log user in
            login(request, user)
    context = {'form': form}
    return render(request, 'classrooms/authentication/register.html', context)

@already_authenticated_user
def login_form(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect(home)
    else: 
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'classrooms/authentication/login.html', context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect(login_form)
        

