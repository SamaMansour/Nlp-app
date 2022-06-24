import uuid
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
from .helpers import send_forget_password_mail


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

# change password
def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(
            forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login')

    except Exception as e:
        print(e)
    return render(request, 'accounts/change-password.html', context)

# forget password
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('accounts/forget-password/')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('accounts/forget-password/')

    except Exception as e:
        print(e)
    return render(request, 'accounts/forget-password.html')





@login_required
def profile(request):
    return render(request, 'Dashboard/index.html')




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
    
    for i in groups:
        print (i.name)
    if check_admin(request.user):
        return render(request, 'group/create.html', context={'groups': groups})
    else:
        return render(request, 'group/user.html', context={'groups': groups})




    
    
        



# Delete Group

def delGroups (request,name):
    b =Group.objects.filter(name=name)
    b.delete()
    return render(request, 'group/create.html')




 # join Group 
def join(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        group.members.add(request.user)
        group.save()
        return redirect('/groups/' + str(group_id))
    else:
        return render(request, '/group/user.html', {'group': group})
 # leave Group 


def leave(request, user_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, pk=group_id)
        if request.user in group.members.all():
            group.members.remove(request.user)
            group.save()
            return redirect('home')
            return HttpResponse("You have been removed successfully " + str(user.username))

    else:
        return render(request, '/group/user.html')
