from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .forms import NewUserForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CaseForm,  UserGroupForm
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group, User
from .models import *

# Create your views here.

# HomeView


def HomeView(request, *args, **kwargs):
    return render(request, "home.html", {})

# DashboardView

def DashboardView(request, *args, **kwargs):
    return render(request, "Dashboard\index.html", {})


# SignupView
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="accounts/signup.html", context={"register_form": form})

# loginView
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('signup')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="accounts/login.html",
                  context={"form": form})


# logout
def logout_request(request):
    logout(request)
    return redirect('/')


@login_required
def profile(request):
    return render(request, 'Dashboard/index.html')




# Case view





# check Admin
def check_admin(User):
       return User.is_superuser

# create Group
@login_required(login_url='login')
def createGroup(request):
	if request.method == 'POST':
		name =request.POST.get('name')
		if name != "":
			if len(Group.objects.filter(name=name)) ==0:
				group=Group(name=name)
				group.save()
	return render(request,'group/create.html')

# List Groups

def getGroups(request):

    groups = Group.objects.all()
    if (check_admin(User)):
        for i in groups:
            print (i.name)
        return render(request,'group/create.html',context= {'groups':groups})
    else:
        return render(request, 'group/user.html', context={'groups': groups})
        



# Delete Group

def delGroups (request,name):
    b =Group.objects.filter(name=name)
    b.delete()
    return render(request, 'group/create.html')




# join Group 
def joinGroup(request,name):
     groups = Group.objects.all()
     user = User.objects.get(username="samamansour") 

     if request.method == 'POST':
        user.groups.add("groupal")
        user.save()
        
     else:
        return render(request,'group/user.html', {'groups': groups})



